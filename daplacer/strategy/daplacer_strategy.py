from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
)

from eclypse.placement.strategies import PlacementStrategy

from daplacer.utils import (
    ASSERT,
    DAP_FILE,
    DYNAMICS,
    PL_ALL_FILE,
    PL_RELAXED_FILE,
    RETRACT,
    consult,
    timed_query,
)

from .pl_engine import pl_process

if TYPE_CHECKING:
    from eclypse.graph import (
        Application,
        Infrastructure,
    )
    from eclypse.placement import (
        Placement,
        PlacementView,
    )
    from swiplserver import PrologThread


def place_bindings(
    infrastructure: Infrastructure, application: Application
) -> Dict[str, Any]:
    all_things = list(infrastructure.graph.get("sensors", {}).keys()) + list(
        infrastructure.graph.get("actuators", {}).keys()
    )
    partial_placement = {}
    bindings = infrastructure.graph.get("dataBindings", [])
    for n, nthings in infrastructure.nodes(data="IoT"):
        if nthings:
            for t in nthings:
                if t in all_things:
                    for _, req_id, thg_id in bindings:
                        if thg_id == t and req_id in application.graph["Requirements"]:
                            partial_placement[req_id] = n
                            all_things.remove(t)
                            break
    return partial_placement


class DAPlacerStrategy(PlacementStrategy):

    def __init__(
        self,
        prolog: PrologThread,
        relaxed: bool = False,
        timeout: Optional[int] = None,
    ):
        self.prolog = prolog
        self.exec_time = float("inf")
        self.n_relaxed = float("inf")
        self.inferences = float("inf")

        self.timeout = timeout
        self.relaxed = relaxed
        self.first_iteration = True

    def place(
        self,
        infrastructure: Infrastructure,
        application: Application,
        _: Dict[str, Placement],
        __: PlacementView,
    ) -> Dict[Any, Any]:

        if self.first_iteration:
            for d in DYNAMICS:
                timed_query(self.prolog, f"dynamic {d}")

            consult(self.prolog, application.graph["file"])
            consult(self.prolog, infrastructure.graph["file"])
            consult(self.prolog, DAP_FILE)
            consult(self.prolog, PL_RELAXED_FILE if self.relaxed else PL_ALL_FILE)
            self.first_iteration = False

        self.sync_edges(application)
        mapping = place_bindings(infrastructure, application)
        self.sync_available_infra(infrastructure)
        service_mapping, self.exec_time, self.inferences, self.n_relaxed = pl_process(
            self.prolog,
            application.name,
            timeout=self.timeout,
        )

        if service_mapping:
            mapping.update(service_mapping)

        return mapping

    def sync_edges(self, app: Application):
        for (src, dst), attr in app.graph["e2e"].items():
            tot_bw = 0
            rates = attr.pop("DataRates", [])
            for data_id, data_rate in rates:
                if data_id not in app.graph["DataTypes"]:
                    raise ValueError(f"DataId {data_id} not found in DataTypes.")
                data_size = app.graph["DataTypes"][data_id]["Size"]
                tot_bw += data_rate * data_size

            if src not in app.nodes:
                app.add_node(src)

            if dst not in app.nodes:
                app.add_node(dst)

            app.add_edge(src, dst, latency=attr["latency"], bandwidth=tot_bw)

    def sync_available_infra(self, infr: Infrastructure):
        timed_query(self.prolog, RETRACT.format("node(_, _, _, _, _)"))
        for n, nattr in infr.nodes(data=True):
            pl_str = ASSERT.format(
                f"node({n}, {nattr['Sw']}, ({nattr['Cpu']}, {nattr['Ram']}, "
                f"{nattr['Storage']}), {nattr['Sec']}, {nattr['IoT']})"
            )
            timed_query(self.prolog, pl_str)

        timed_query(self.prolog, RETRACT.format("link(_, _, _, _)"))
        for n1, n2, lattr in infr.edges(data=True):
            pl_str = ASSERT.format(
                f"link({n1}, {n2}, {lattr['latency']}, {lattr['bandwidth']})"
            )
            timed_query(self.prolog, pl_str)
