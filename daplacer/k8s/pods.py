from __future__ import annotations

import time
from typing import (
    TYPE_CHECKING,
    Tuple,
)

import kubernetes as k8s
import yaml

from daplacer.utils import (
    APP_FILE,
    APP_NAME,
    APPLICATION,
    CONTAINER_NAME,
    DATA_TYPE,
    MANIFESTS_DIR,
    POD_NAME,
    SCHEDULER_NAME,
    SERVICE,
    consult,
    timed_query,
)

if TYPE_CHECKING:
    from swiplserver import PrologThread


def infer_image(swreqs: list[str]) -> str:
    swreqs = [s.lower() for s in swreqs]
    if "python" in swreqs and "mysql" in swreqs:
        return "python:3.10"
    if "mysql" in swreqs:
        return "mysql:8.0"
    if "python" in swreqs:
        return "python:3.10"
    if "ubuntu" in swreqs:
        return "ubuntu:22.04"
    return "alpine:latest"


def parse_hw(hw_tuple: Tuple[int, int, int]) -> Tuple[str, str, str]:
    cpu_cores, ram_gb, storage_gb = hw_tuple
    return str(cpu_cores), f"{ram_gb}Gi", f"{storage_gb}Gi"


def parse_requirements(
    prolog: PrologThread,
    service_id: str,
) -> Tuple[list[str], list[str]]:
    data_query = SERVICE.format(
        service_id=service_id,
        sw="_",
        cpu="_",
        ram="_",
        storage="_",
        data_ids="DataIds",
        migration_cost="_",
    )
    data_ids = timed_query(prolog, query=data_query)[0]["DataIds"]

    sec_reqs = set()
    for d in data_ids:
        sec_query = DATA_TYPE.format(data_id=d, size="_", sec_reqs="Secs")
        result = timed_query(prolog, query=sec_query)[0]["Secs"]
        sec_reqs.update(result)

    return data_ids, list(sec_reqs)


def build_deployment_yaml(
    service_id: str,
    swreqs: list[str],
    hwreqs: Tuple[int, int, int],
    data_ids: list[str],
    sec_reqs: list[str],
) -> dict:
    cpu, memory, storage = parse_hw(hwreqs)
    image = infer_image(swreqs)
    sid = service_id.lower()

    labels = {
        "app": sid,
        "service": service_id,
    }

    for sw in swreqs:
        labels[f"sw.{sw}"] = "true"
    for sec in sec_reqs:
        labels[f"qos.{sec}"] = "true"
    for data in data_ids:
        labels[f"data.{data}"] = "true"

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": POD_NAME.format(sid),
            "labels": labels,
        },
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": sid}},
            "template": {
                "metadata": {"labels": labels},
                "spec": {
                    "schedulerName": SCHEDULER_NAME,
                    "containers": [
                        {
                            "name": CONTAINER_NAME.format(sid),
                            "image": image,
                            "command": ["sleep", "3600"],
                            "resources": {
                                "requests": {
                                    "cpu": cpu,
                                    "memory": memory,
                                    "ephemeral-storage": storage,
                                }
                            },
                        }
                    ],
                },
            },
        },
    }

    return deployment


def apply_deployment(dep_yaml: dict):
    k8s.config.load_kube_config()
    v1 = k8s.client.AppsV1Api()

    dep_name = dep_yaml["metadata"]["name"]
    namespace = dep_yaml["metadata"].get("namespace", "default")

    try:
        v1.read_namespaced_deployment(name=dep_name, namespace=namespace)
        print(f"'{dep_name}' already exists. Deleting...")

        v1.delete_namespaced_deployment(name=dep_name, namespace=namespace)

        for _ in range(30):
            time.sleep(0.5)
            try:
                v1.read_namespaced_deployment(name=dep_name, namespace=namespace)
            except k8s.client.exceptions.ApiException as e:
                if e.status == 404:
                    break
        else:
            print(f"Warning: Timeout waiting for deployment {dep_name} deletion.")

    except k8s.client.exceptions.ApiException as e:
        if e.status != 404:
            print(f"Error checking deployment {dep_name}: {e}")
            return

    try:
        v1.create_namespaced_deployment(namespace=namespace, body=dep_yaml)
        print(f"Created deployment {dep_name}")
    except k8s.client.exceptions.ApiException as e:
        print(f"Error creating deployment {dep_name}: {e}")


def write_manifest(dep_yaml: dict):
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = MANIFESTS_DIR / f"{dep_yaml['metadata']['name']}.yaml"
    with open(filename, "w") as f:
        yaml.dump(dep_yaml, f, sort_keys=False)
        print(f"Deployment {dep_yaml['metadata']['name']} saved to {filename}")


def generate_pods(prolog: PrologThread, apply: bool = False):
    consult(prolog, APP_FILE)

    result = timed_query(
        prolog=prolog,
        query=APPLICATION.format(app_id=APP_NAME, service_ids="Services"),
    )

    if not result:
        raise ValueError(f"Application '{APP_NAME}' not found in knowledge base.")

    services = result[0]["Services"]

    for service_id in services:
        query = SERVICE.format(
            service_id=service_id,
            sw="SW",
            cpu="CPU",
            ram="RAM",
            storage="Storage",
            data_ids="_",
            migration_cost="_",
        )
        res = timed_query(prolog, query)[0]
        swreqs = res["SW"]
        hwreqs = (res["CPU"], res["RAM"], res["Storage"])

        data_ids, sec_reqs = parse_requirements(prolog, service_id)

        dep_yaml = build_deployment_yaml(service_id, swreqs, hwreqs, data_ids, sec_reqs)

        if apply:
            apply_deployment(dep_yaml)
        else:
            write_manifest(dep_yaml)
