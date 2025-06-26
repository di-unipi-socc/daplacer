from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional

import prolog_to_networkx as ptn
from eclypse.graph import Infrastructure

from daplacer.infrastructures.handlers import get_handlers

infra_cfg = ptn.FactsConfig(
    node_facts=["node", "nodeType", "location", "provider"],
    edge_facts="link",
)

# Soglie globali
infra_cfg.add_fact("bwTh", "Threshold")

# Costi e CI
infra_cfg.add_fact("nodeCI", "NodeId", "CI")
infra_cfg.add_fact("nodeCost", "NodeId", "Cost")

# Nodes
infra_cfg.add_node_fact("node", "Sw", ("Cpu", "Ram", "Storage"), "Sec", "IoT")

# Link
infra_cfg.add_edge_fact("link", "latency", "bandwidth")

# Things
infra_cfg.add_fact("sensor", "SensorId", "SensorType", "Data")
infra_cfg.add_fact("actuator", "ActuatorId", "ActuatorType")

# Binding
infra_cfg.add_fact("dataBinding", "ServiceId", "RequirementId", "ThingId")


def get_infrastructure(
    n: int,
    seed: int,
    topology: Optional[Literal["BA", "ER"]] = None,
    node_update_policy: Optional[Callable] = None,
    edge_update_policy: Optional[Callable] = None,
    node_assets: Optional[Dict[str, Any]] = None,
    edge_assets: Optional[Dict[str, Any]] = None,
    path_assets_aggregators: Optional[Dict[str, Callable[[List[Any]], Any]]] = None,
) -> Infrastructure:

    parser = ptn.PrologGraphParser(infra_cfg, handlers=get_handlers())

    infra = Infrastructure(
        infrastructure_id=f"infr{n}-{seed}",
        node_update_policy=node_update_policy,
        edge_update_policy=edge_update_policy,
        node_assets=node_assets,
        edge_assets=edge_assets,
        path_assets_aggregators=path_assets_aggregators,
        seed=seed,
        resource_init="max",
    )

    infra.graph["file"] = (
        Path(__file__).parent
        / (topology if topology is not None else "")
        / f"infr{n}-{seed}.pl"
    )

    parser.parse(file_path=infra.graph["file"], graph=infra)

    return infra
