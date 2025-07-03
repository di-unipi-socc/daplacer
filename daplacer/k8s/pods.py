from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Tuple,
)

import kubernetes as k8s
import yaml
from swiplserver import PrologMQI

from daplacer.utils import (
    APP_FILE,
    APP_NAME,
    APPLICATION,
    CONSULT,
    DATA_TYPE,
    INFR_FILE,
    MANIFESTS_DIR,
    SERVICE,
    timed_query,
)

if TYPE_CHECKING:
    from swiplserver import PrologThread


def infer_image(swreqs):
    swreqs = [s.lower() for s in swreqs]
    if "python" in swreqs and "mysql" in swreqs:
        return "python:3.10"
    if "mysql" in swreqs:
        return "mysql:8.0"
    if "python" in swreqs:
        return "python:3.10"
    if "ubuntu" in swreqs:
        return "ubuntu:22.04"
    return "alpine:latest"  # fallback


def parse_hw(hw_tuple: Tuple[int, int, int]) -> Tuple[str, str, str]:
    cpu_cores, ram_gb, storage_gb = hw_tuple
    return str(cpu_cores), f"{ram_gb}Gi", f"{storage_gb}Gi"


def parse_requirements(service_id: str, prolog: PrologThread):
    data_query = SERVICE.format(
        service_id=service_id,
        sw="_",
        cpu="_",
        ram="_",
        storage="_",
        data_ids="DataIds",
        migration_cost="_",
    )
    data_ids = timed_query(prolog=prolog, query=data_query)[0]["DataIds"]

    sec_reqs = set()
    for d in data_ids:
        data_type_query = DATA_TYPE.format(data_id=d, size="_", sec_reqs="Secs")
        result = timed_query(prolog=prolog, query=data_type_query)[0]["Secs"]
        sec_reqs.update(result)
    return data_ids, list(sec_reqs)


def build_pod_yaml(service_id, swreqs, hwreqs, data_ids, sec_reqs):
    cpu, memory, storage = parse_hw(hwreqs)
    image = infer_image(swreqs)

    labels = {
        "service": service_id,
        "software": ",".join(swreqs),
        "qos-sec": ",".join(sec_reqs),
        "data": ",".join(data_ids),
    }

    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": f"{service_id}-pod", "labels": labels},
        "spec": {
            "schedulerName": "daplacer-scheduler",
            "containers": [
                {
                    "name": f"{service_id}-container",
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
    }

    return pod


def apply_pod(pod_yaml):
    """Applica un pod al cluster"""
    k8s.config.load_kube_config()
    v1 = k8s.client.CoreV1Api()
    try:
        v1.create_namespaced_pod(namespace="default", body=pod_yaml)
        print(f"Created pod {pod_yaml['metadata']['name']}")
    except k8s.client.exceptions.ApiException as e:
        print(f"❌ Error creating pod {pod_yaml['metadata']['name']}: {e}")


def write_pod(pod_yaml):
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = MANIFESTS_DIR / f"{pod_yaml['metadata']['name']}.yaml"
    with open(filename, "w") as f:
        yaml.dump(pod_yaml, f, sort_keys=False)
        print(f"Pod {pod_yaml['metadata']['name']} saved to {filename}")


def generate_pods(apply: bool = False):
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog:
            timed_query(prolog=prolog, query=CONSULT.format(APP_FILE), clean=False)
            print(APP_FILE)

            r = timed_query(
                prolog=prolog,
                query=APPLICATION.format(app_id=APP_NAME, service_ids="Services"),
            )
            if not r:
                raise ValueError(
                    f"Application '{APP_NAME}' not found in knowledge base."
                )

            services = r[0]["Services"]
            for service_id in services:
                q = SERVICE.format(
                    service_id=service_id,
                    sw="SW",
                    cpu="CPU",
                    ram="RAM",
                    storage="Storage",
                    data_ids="_",
                    migration_cost="_",
                )
                res = list(prolog.query(q))[0]
                swreqs = res["SW"]
                hwreqs = (res["CPU"], res["RAM"], res["Storage"])

                data_ids, sec_reqs = parse_requirements(service_id, prolog)

                pod_yaml = build_pod_yaml(
                    service_id, swreqs, hwreqs, data_ids, sec_reqs
                )
                if apply:
                    apply_pod(pod_yaml)
                else:
                    write_pod(pod_yaml)
