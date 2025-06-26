from __future__ import annotations

from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Optional,
)

import prolog_to_networkx as ptn
from eclypse.graph import Application
from prolog_to_networkx import FactsConfig

from daplacer.applications.handlers import get_handlers

if TYPE_CHECKING:
    from networkx.classes.reportviews import (
        EdgeView,
        NodeView,
    )

app_cfg = FactsConfig(
    graph_facts=["application"],
    node_facts=["service", "serviceCost", "serviceCI"],
    edge_facts="e2e",
    graph_id="AppId",
    node_id="ServiceId",
)

app_cfg.add_graph_fact("application", "ServiceIds")

app_cfg.add_fact("dataType", "DataId", "Size", "SecReqs")
app_cfg.add_fact("requirement", "ReqId", "Type", "DataIds")

app_cfg.add_node_fact(
    "service", "Sw", ("Cpu", "Ram", "Storage"), "DataIds", "MigrationCost"
)
app_cfg.add_node_fact("serviceCost", "MaxCost")
app_cfg.add_node_fact("serviceCI", "MaxCI")

app_cfg.add_edge_fact("e2e", "latency", "DataRates")


def get_application(
    application_id: str,
    node_update_policy: Optional[Callable[[NodeView], None]] = None,
    edge_update_policy: Optional[Callable[[EdgeView], None]] = None,
    node_assets: Optional[Dict[str, Any]] = None,
    edge_assets: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
) -> Application:
    """Parse the knowledge base and return the application graph,
    by its application_id.
    """

    parser = ptn.PrologGraphParser(app_cfg, handlers=get_handlers())
    app = Application(
        application_id=application_id,
        node_update_policy=node_update_policy,
        edge_update_policy=edge_update_policy,
        node_assets=node_assets,
        edge_assets=edge_assets,
        seed=seed,
    )
    app.graph["file"] = Path(__file__).parent / "prolog" / f"{application_id}.pl"
    parser.parse(file_path=app.graph["file"], graph=app)
    return app
