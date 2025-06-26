from pathlib import Path
from random import Random
from typing import List

import networkx as nx
from numpy import log2

from daplacer.utils import INFRS_DIR

LAT_MIN, LAT_MAX = 2, 20
BW_MIN, BW_MAX = 100, 500
TYPES_PROBS = [0.30, 0.25, 0.2, 0.15, 0.10]
SEC_CAPS = ["encryption", "auth"]
NODE_TYPES = {
    "smartphone": {
        "sw": ["ubuntu", "python"],
        "cpu": 2.4,
        "ram": 4,
        "storage": 32,
    },
    "accesspoint": {
        "sw": ["ubuntu", "mySQL"],
        "cpu": 3,
        "ram": 6,
        "storage": 128,
    },
    "cabinet": {
        "sw": ["python", "mySQL"],
        "cpu": 4,
        "ram": 8,
        "storage": 256,
    },
    "isp": {
        "sw": ["ubuntu", "mySQL", "python"],
        "cpu": 5,
        "ram": 16,
        "storage": 512,
    },
    "cloud": {
        "sw": ["ubuntu", "mySQL", "python"],
        "cpu": 128,
        "ram": 64,
        "storage": 1024,
    },
}

NODE_COST_RANGES = {
    "cloud": (5.0, 7.0),
    "isp": (3.5, 5),
    "cabinet": (2.0, 3.5),
    "accesspoint": (1.0, 2.0),
    "smartphone": (0.5, 1.5),
}

NODE_CI_RANGE = (0.04, 1)

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

# LINK_PROFILES = {
#     ("cloud", "cloud"): (20, 1000),
#     ("cloud", "isp"): (110, 1000),
#     ("cloud", "cabinet"): (135, 100),
#     ("cloud", "accesspoint"): (100, 50),
#     ("cloud", "smartphone"): (150, 40),
#     ("isp", "isp"): (20, 1000),
#     ("isp", "cabinet"): (25, 500),
#     ("isp", "accesspoint"): (38, 50),
#     ("isp", "smartphone"): (20, 1000),
#     ("cabinet", "cabinet"): (20, 1000),
#     ("cabinet", "accesspoint"): (13, 50),
#     ("cabinet", "smartphone"): (15, 35),
#     ("accesspoint", "accesspoint"): (10, 50),
#     ("accesspoint", "smartphone"): (2, 70),
#     ("smartphone", "smartphone"): (15, 50),
# }


# def get_link_profile(type1, type2):
#     return LINK_PROFILES.get((type1, type2)) or LINK_PROFILES.get((type2, type1))


class InfraBuilder(nx.Graph):

    def __init__(self, n_nodes: int, bw_threshold: int = 3, seed=42, generator="ba"):
        super().__init__()
        self.generator = generator
        self.seed = seed
        self.labels = {}
        self.bw_threshold = bw_threshold
        self.types = list(NODE_TYPES.keys())
        self.rng = Random(seed)
        self.file = "infr{}-{}.pl".format(n_nodes, self.seed)
        self.generate_topology(n_nodes)

    def generate_topology(self, n: int):
        if self.generator == "ba":
            g = nx.barabasi_albert_graph(n, int(log2(n)), seed=self.seed)
        elif self.generator == "er":
            g = nx.gnp_random_graph(n, 0.4, seed=self.seed)
        else:
            raise ValueError(f"Unsupported generator: {self.generator}")

        type_counts = {t: 0 for t in self.types}
        label_map = {}
        for node in g.nodes:
            t = self.rng.choices(self.types, weights=TYPES_PROBS, k=1)[0]
            idx = type_counts[t]
            nid = f"{t}{idx}"
            type_counts[t] += 1
            label_map[node] = nid

            spec = NODE_TYPES[t]
            cost = round(self.rng.uniform(*NODE_COST_RANGES[t]), 2)
            ci = round(self.rng.uniform(*NODE_CI_RANGE), 2)
            self.add_node(
                nid,
                nodeType=t,
                cost=cost,
                ci=ci,
                things=[],
                sec=SEC_CAPS,
                **spec,
            )

        for u, v in g.edges:
            u_id, v_id = label_map[u], label_map[v]
            latency = self.rng.randint(LAT_MIN, LAT_MAX)
            bandwidth = self.rng.randint(BW_MIN, BW_MAX)
            self.add_edge(u_id, v_id, lat=latency, bw=bandwidth)
            self.add_edge(v_id, u_id, lat=latency, bw=bandwidth)
            # t1, t2 = self.nodes[u_id]["nodeType"], self.nodes[v_id]["nodeType"]
            # lat, bw = get_link_profile(t1, t2)
            # self[u_id][v_id]["lat"] = lat
            # self[u_id][v_id]["bw"] = bw

        for node_id in self.nodes:
            self.set_things(node_id)

    def set_things(self, nid):
        things = []
        if nid == "smartphone0":
            things = ["video3", "door27"]
        elif nid == "smartphone1":
            things = ["cam20"]
        elif nid == "smartphone2":
            things = ["glass4"]
        elif nid == "accesspoint0":
            things = ["art42", "vst38"]
        elif nid == "accesspoint1":
            things = ["loc38"]
        self.nodes[nid]["things"] = things

    def upload(self):
        path = Path(INFRS_DIR) / self.generator.upper()
        self.file = path / self.file
        self.file.parent.mkdir(parents=True, exist_ok=True)

        with self.file.open("w") as f:
            output = f"bwTh({self.bw_threshold}).\n\n"
            # node/5
            for n, d in self.nodes(data=True):
                output += (
                    f"node({n}, {d['sw']}, ({d['cpu']}, {d['ram']}, {d['storage']}), "
                    f"{d['sec']}, {d['things']}).\n"
                ).replace("'", "")
            output += "\n"

            # nodeCost/2
            for n, d in self.nodes(data=True):
                output += f"nodeCost({n}, {d['cost']}).\n"
            output += "\n"

            # nodeCI/2
            for n, d in self.nodes(data=True):
                output += f"nodeCI({n}, {d['ci']}).\n"
            output += "\n"

            # link/4 (both directions)
            for u, v, d in self.edges(data=True):
                output += f"link({u}, {v}, {d['lat']}, {d['bw']}).\n"
                output += f"link({v}, {u}, {d['lat']}, {d['bw']}).\n"
            output += "\n"
            f.write(APPENDIX + output)
        print(f"Infra file saved to {self.file}")


def generate_infrastructures(nodes: List[int], seeds: List[int], verbose=False):
    for n in nodes:
        for seed in seeds:
            builder = InfraBuilder(n, seed=seed)
            builder.upload()
            if verbose:
                print(f"Generated infrastructure with {n} nodes and seed {seed}.")
