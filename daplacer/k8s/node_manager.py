from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
)

import docker
from kubernetes import client

from daplacer.builder import BW_MIN
from daplacer.utils import (
    ASSERT,
    BW_MAX,
    LAT_MAX,
    LAT_MIN,
    LINK,
    NODE,
    NODE_CI,
    NODE_UNIT_COST,
    RETRACT,
    SEC_CAPS,
    SW_CAPS,
    parse_prolog,
    timed_query,
    to_gib,
)

if TYPE_CHECKING:
    from random import Random

    from kubernetes.client import CoreV1Api
    from swiplserver import PrologThread

# Sensors + Actuators
IOT = ["art42", "vst38", "cam20"] + ["video3", "door27", "glass4", "loc38"]

TYPES_PROBS = [0.30, 0.25, 0.2, 0.15, 0.10]

NODE_UNIT_COSTS = {
    "smartphone": (0.002, 0.0005, 0.0001),
    "accesspoint": (0.005, 0.0008, 0.0001),
    "cabinet": (0.01369366, 0.00150366, 0.0002),
    "isp": (0.052624, 0.0057785, 0.0002),
    "cloud": (0.052624, 0.0057785, 0.0002),
}

NODE_CI_RANGE = (0.04, 0.8)


def get_nodes_docker():
    client_docker = docker.from_env()
    containers = client_docker.containers.list(all=True)
    nodes = []

    for c in containers:
        if not c.name.startswith("minikube"):
            continue
        nodes.append(c.name)

    return nodes


def get_nodes_k8s(v1: CoreV1Api):
    try:
        nodes = v1.list_node().items
        return [node.metadata.name for node in nodes]
    except client.exceptions.ApiException as e:
        print(f"Error fetching nodes: {e}")
        return []


def get_nodes(use_docker: bool = False) -> List[str]:
    return get_nodes_docker() if use_docker else get_nodes_k8s()


def get_node_info_docker(node_id: str):
    client_docker = docker.from_env()

    try:
        container = client_docker.containers.get(node_id)
        info = container.attrs

        return {
            "name": container.name,
            "cpu": int(info["HostConfig"].get("NanoCpus", 0) / 1e9),
            "ram": int(info["HostConfig"].get("Memory", 0)) / (1024**3),
            "storage": 50,  # stimato
        }
    except docker.errors.NotFound:
        print(f"Docker node '{node_id}' not found.")
        return None
    except Exception as e:
        print(f"Error reading Docker node '{node_id}': {e}")
        return None


def get_node_info_k8s(node_id: str, v1: CoreV1Api):

    try:
        node = v1.read_node(name=node_id)
        alloc = node.status.allocatable

        return {
            "name": node.metadata.name,
            "cpu": int(alloc.get("cpu", "1")),
            "ram": to_gib(alloc.get("memory", "0Ki")),
            "storage": to_gib(alloc.get("ephemeral-storage", "0Ki")),
        }
    except client.exceptions.ApiException as e:
        print(f"Error fetching node '{node_id}': {e}")
        return None


def get_node_info(node_id: str, v1: CoreV1Api, use_docker: bool = False):
    return (
        get_node_info_docker(node_id) if use_docker else get_node_info_k8s(node_id, v1)
    )


def add_node(
    node_id: str,
    prolog: PrologThread,
    rand: Random,
    node_info: Dict[str, Any],
    use_docker: bool = False,
):
    name = node_id.replace("-", "_")
    if name == "minikube":
        print("Skipping 'minikube' node as it is reserved.")
        return

    nq = timed_query(prolog, f"node({name}, _, _, _, _)")
    if nq:
        print(f"Node '{name}' already exists in Prolog. Skipping addition.")
        return
    cpu = node_info["cpu"]
    ram = node_info["ram"]
    storage = node_info["storage"]
    devices = []
    if IOT != []:
        n_to_assign = min(len(IOT), rand.randint(1, 3))
        rand.shuffle(IOT)
        devices = rand.sample(IOT, n_to_assign)
        for d in devices:
            IOT.remove(d)

    devices = str(devices).replace("'", "")
    ntype = rand.choices(list(NODE_UNIT_COSTS.keys()), weights=TYPES_PROBS, k=1)[0]
    cpu_cost, ram_cost, storage_cost = NODE_UNIT_COSTS[ntype]
    ci = round(rand.uniform(*NODE_CI_RANGE), 2)

    node_query = NODE.format(
        node_id=name,
        sw=SW_CAPS,
        cpu=cpu,
        ram=ram,
        storage=storage,
        sec_caps=SEC_CAPS,
        things=devices,
    )

    node_ci_query = NODE_CI.format(node_id=name, ci=ci)
    node_cost_query = NODE_UNIT_COST.format(
        node_id=name,
        cpu_cost=cpu_cost,
        ram_cost=ram_cost,
        storage_cost=storage_cost,
    )

    timed_query(prolog, ASSERT.format(node_query))
    timed_query(prolog, ASSERT.format(node_ci_query))
    timed_query(prolog, ASSERT.format(node_cost_query))

    print("-----------------")
    print("Asserted node facts:")
    print(node_query)
    print(node_ci_query)
    print(node_cost_query)

    # Randomly assign e2e links from new node to all the others

    links = []
    nodes = [n.replace("-", "_") for n in get_nodes(use_docker=use_docker)]
    for other_node in nodes:
        if other_node == name:
            continue
        latency = rand.randint(LAT_MIN, LAT_MAX)
        bandwidth = rand.randint(BW_MIN, BW_MAX)
        links.append(
            LINK.format(u=name, v=other_node, latency=latency, bandwidth=bandwidth)
        )
        links.append(
            LINK.format(u=other_node, v=name, latency=latency, bandwidth=bandwidth)
        )

    for lq in links:
        timed_query(prolog, ASSERT.format(lq))


def delete_node(node_id: str, prolog: PrologThread):
    name = node_id.replace("-", "_")
    node_query = f"node({name}, _, _, _, Things)"
    r = timed_query(prolog, node_query)
    if r:
        r = parse_prolog(r[0])
        print(r)
        IOT.extend(r["Things"])
    timed_query(prolog, RETRACT.format(f"node({name}, _, _, _, _)"))
    timed_query(prolog, RETRACT.format(f"nodeCI({name}, _)"))
    timed_query(prolog, RETRACT.format(f"nodeUnitCost({name}, _, _, _)"))
    timed_query(prolog, RETRACT.format(f"link({name}, _, _, _)"))
    timed_query(prolog, RETRACT.format(f"link(_, {name}, _, _)"))
    print(f"Node {name} deleted from Prolog and IOT devices updated: {IOT}")

    print(timed_query(prolog, "node(N, _, _, _, _)"))


def update_node(node_id: str, prolog: PrologThread):
    pass
