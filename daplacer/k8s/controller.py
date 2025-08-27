from __future__ import annotations

from random import Random
from typing import TYPE_CHECKING

from kubernetes import watch

from daplacer.k8s.node_manager import (
    add_node,
    delete_node,
    get_node_info,
    update_node,
)
from daplacer.utils import load_api

if TYPE_CHECKING:
    from kubernetes.client import CoreV1Api

from swiplserver import PrologThread


def handle_node_event(
    event,
    prolog: PrologThread,
    rand: Random,
    v1: CoreV1Api,
    use_docker: bool = False,
):
    obj = event["object"]
    name = obj.metadata.name
    evt = event["type"]

    node_info = get_node_info(name, v1, use_docker=use_docker)

    if evt == "ADDED":
        add_node(name, prolog, rand, node_info, use_docker=use_docker)
    elif evt == "DELETED":
        delete_node(name, prolog)
    elif evt == "MODIFIED":
        update_node(name, prolog)
        print("-----------------")
        print(f"Node {name} modified, updating...")
        print(f"Node Status: {obj.status.conditions}")
    else:
        print(f"Unhandled event type: {evt} for node {name}")


def controller_loop(prolog: PrologThread, seed: int, use_docker: bool = False):
    r = Random(seed)
    v1 = load_api()
    w = watch.Watch()

    try:
        for event in w.stream(v1.list_node, timeout_seconds=0):
            handle_node_event(event, prolog, r, v1, use_docker=use_docker)
    finally:
        print("Node controller stopped")
