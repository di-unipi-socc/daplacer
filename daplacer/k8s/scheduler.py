from __future__ import annotations

import time
from typing import TYPE_CHECKING

from kubernetes import client

from daplacer.k8s.pl_engine import pl_process
from daplacer.utils import (
    APP_FILE,
    APP_NAME,
    DAP_FILE,
    DYNAMICS,
    INFR_NAME,
    INFRS_DIR,
    PL_RELAXED_FILE,
    SCHEDULER_NAME,
    SLEEP_TIME,
    consult,
    load_api,
    timed_query,
)

if TYPE_CHECKING:
    from kubernetes.client import CoreV1Api
    from swiplserver import PrologThread


def get_pending_pods(v1: CoreV1Api, scheduler_name=SCHEDULER_NAME):
    pods = v1.list_pod_for_all_namespaces(
        field_selector=f"spec.schedulerName={scheduler_name}"
    )
    return [
        p
        for p in pods.items
        if p.status.phase == "Pending" and p.status.conditions is None
    ]


def bind_deployment(v1: CoreV1Api, pod, node_name):
    target = client.V1ObjectReference(kind="Node", api_version="v1", name=node_name)
    meta = client.V1ObjectMeta(name=pod.metadata.name, namespace=pod.metadata.namespace)
    binding = client.V1Binding(api_version="v1", target=target, metadata=meta)
    try:
        v1.create_namespaced_binding(namespace=pod.metadata.namespace, body=binding)
        print(f"Pod '{pod.metadata.name}' has been scheduled to node '{node_name}'")
    except client.exceptions.ApiException as e:
        print(f"Error binding pod '{pod.metadata.name}': {e}")


def scheduler_loop(prolog: PrologThread, n_nodes: int, seed: int):
    print(f"Starting {SCHEDULER_NAME}...")
    v1 = load_api()

    for fact in DYNAMICS:
        timed_query(prolog, f"dynamic {fact}")

    consult(prolog, APP_FILE)
    infr_file = INFRS_DIR / INFR_NAME.format(nodes=n_nodes, seed=seed)
    consult(prolog, infr_file)
    consult(prolog, DAP_FILE)
    consult(prolog, PL_RELAXED_FILE)

    while True:
        pending_pods = get_pending_pods(v1)
        print(f"Pending pods: {[p.metadata.name for p in pending_pods]}")

        if not pending_pods:
            time.sleep(SLEEP_TIME)
            continue

        assignments, _, _ = pl_process(app_name=APP_NAME, prolog=prolog)

        for pod_name, node in assignments.items():
            for pod in pending_pods:
                if pod_name.lower() in pod.metadata.name:
                    try:
                        node_name = node.replace("_", "-")
                        bind_deployment(v1, pod, node_name)
                    except ValueError as e:
                        if "must not be `None`" in str(e):
                            # traceback.print_exc()
                            pass
                        else:
                            print(f"Error binding pod '{pod.metadata.name}': {e}")
        time.sleep(SLEEP_TIME)
