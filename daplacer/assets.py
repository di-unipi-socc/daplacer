from eclypse.graph.assets import (
    Additive,
    Concave,
    Symbolic,
)
from eclypse.graph.assets.defaults import get_default_path_aggregators
from eclypse.utils.constants import (
    MAX_BANDWIDTH,
    MAX_FLOAT,
    MAX_LATENCY,
    MIN_BANDWIDTH,
    MIN_FLOAT,
    MIN_LATENCY,
)


node_assets = {
    "Cpu": Additive(MIN_FLOAT, MAX_FLOAT),
    "Ram": Additive(MIN_FLOAT, MAX_FLOAT),
    "Storage": Additive(MIN_FLOAT, MAX_FLOAT),
    "Sw": Symbolic([], ["ubuntu", "python", "mySQL"]),
    "Sec": Symbolic([], ["encryption", "auth"]),
}

edge_assets = {
    "latency": Concave(MAX_LATENCY, MIN_LATENCY),
    "bandwidth": Additive(MIN_BANDWIDTH, MAX_BANDWIDTH),
}

__all__ = [
    "node_assets",
    "edge_assets",
    "get_default_path_aggregators",
]
