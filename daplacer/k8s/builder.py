from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

import docker
from kubernetes import (
    client,
    config,
)

from daplacer.utils import SEC_CAPS, SW_CAPS, to_gib

if TYPE_CHECKING:
    from random import Random

# === CONFIG ===
BW_THRESHOLD = 5  # Mbps
TYPES_PROBS = [0.30, 0.25, 0.2, 0.15, 0.10]

APPENDIX = (
    "dataBinding(interface, rCam, cam20).\n"
    "dataBinding(interface, rVid, video3).\n"
    "dataBinding(dataStorage, rVst, vst38).\n"
    "dataBinding(dataStorage, rArt, art42).\n"
    "dataBinding(dataStorage, rLoc, loc38).\n"
    "dataBinding(controller, rGls, glass4).\n"
    "dataBinding(controller, rDor, door27).\n\n"
    "sensor(art42, heat, [artStats]).\n"
    "sensor(vst38, smartphone, [visitorStats, videoStream]).\n"
    "sensor(cam20, camera, [videoStream]).\n"
    "actuator(video3, display).\n"
    "actuator(door27, smartdoor).\n"
    "actuator(glass4, smartphone).\n"
    "actuator(loc38, location).\n\n"
)

SENSORS = ["art42", "vst38", "cam20"]
ACTUATORS = ["video3", "door27", "glass4", "loc38"]

NODE_UNIT_COSTS = {
    "smartphone": (0.002, 0.0005, 0.0001),
    "accesspoint": (0.005, 0.0008, 0.0001),
    "cabinet": (0.01369366, 0.00150366, 0.0002),
    "isp": (0.052624, 0.0057785, 0.0002),
    "cloud": (0.052624, 0.0057785, 0.0002),
}

NODE_CI_RANGE = (0.04, 0.8)


def get_node_info_k8s():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1.list_node().items


def get_node_info_docker():
    client_docker = docker.from_env()
    containers = client_docker.containers.list(all=True)
    nodes = []

    for c in containers:
        if not c.name.startswith("minikube"):
            continue
        try:
            info = c.attrs
            node_data = {
                "name": c.name,
                "cpus": round(info["HostConfig"].get("NanoCpus", 0) / 1e9, 2),
                "memory_gib": int(info["HostConfig"].get("Memory", 0)) / (1024**3),
                "storage_gib": 50,  # Docker non fornisce questo, impostalo a stima fissa
            }
            nodes.append(node_data)
        except Exception as e:
            print(f"Error reading container {c.name}: {e}")
    return nodes


def generate_node_facts(nodes, rand: Random, use_docker: bool = False):
    node_facts = []
    node_ci_facts = []
    node_cost_facts = []

    if use_docker:
        nodes = get_node_info_docker()
        node_names = [n["name"] for n in nodes]
    else:
        nodes = get_node_info_k8s()
        node_names = [n.metadata.name for n in nodes]

    node_names.remove("minikube")
    rand.shuffle(node_names)

    all_devices = list(SENSORS) + list(ACTUATORS)
    rand.shuffle(all_devices)
    device_assignment = defaultdict(list)

    for idx, device in enumerate(all_devices):
        node_idx = idx % len(node_names)
        device_assignment[node_names[node_idx]].append(device)

    for name in node_names:
        ntype = rand.choices(list(NODE_UNIT_COSTS.keys()), weights=TYPES_PROBS, k=1)[0]
        devices = str(device_assignment[name]).replace("'", "")

        if use_docker:
            node = next(n for n in nodes if n["name"] == name)
            cpu = int(node["cpus"])
            ram = round(node["memory_gib"], 2)
            storage = round(node["storage_gib"], 2)
        else:
            node = next(n for n in nodes if n.metadata.name == name)
            alloc = node.status.allocatable

            cpu = int(alloc.get("cpu", "1"))
            ram = to_gib(alloc.get("memory", "0"))
            storage = to_gib(alloc.get("ephemeral-storage", "0"))

        name = name.replace("-", "_")
        node_facts.append(
            f"node({name}, {SW_CAPS}, ({cpu}, {ram:.2f}, {storage:.2f}), {SEC_CAPS}, {devices})."
        )

        node_ci_facts.append(
            f"nodeCI({name}, {round(rand.uniform(*NODE_CI_RANGE), 2)})."
        )

        cpu_cost, ram_cost, storage_cost = NODE_UNIT_COSTS[ntype]
        node_cost_facts.append(
            f"nodeUnitCost({name}, {cpu_cost}, {ram_cost}, {storage_cost})."
        )

    return node_facts, node_ci_facts, node_cost_facts


def generate_links(nodes, rand: Random):
    links = []
    node_names = [str(n.metadata.name).replace("-", "_") for n in nodes]
    node_names.remove("minikube")
    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            n1 = node_names[i]
            n2 = node_names[j]
            latency = rand.randint(5, 20)  # ms
            bandwidth = rand.randint(100, 1000)  # Mbps
            links.append(f"link({n1}, {n2}, {latency}, {bandwidth}).")
            links.append(f"link({n2}, {n1}, {latency}, {bandwidth}).")
    return links


def write_infrastructure_kb(output_path, rand: Random, use_docker: bool = False):
    output_path = Path(output_path)
    # nodes = get_node_info_k8s()
    # # facts = []

    # # facts.append(f"bwTh({BW_THRESHOLD}).")

    # node_facts, node_ci_facts, node_cost_facts = generate_node_facts(
    #     nodes,
    #     rand=rand,
    #     use_docker=use_docker,
    # )

    # facts = node_facts + [""]
    # facts += node_ci_facts + [""]
    # facts += node_cost_facts + [""]
    # facts += generate_links(nodes, rand=rand)
    # output = "\n".join(facts)

    with open(output_path, "w") as f:
        f.write(f"bwTh({BW_THRESHOLD}).\n\n")
        f.write(f"{APPENDIX}\n\n")
        # f.write(output)

    print(f"KB written to '{output_path}'")
