from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List,
)

from eclypse.report import metric

if TYPE_CHECKING:
    from eclypse.graph import (
        Application,
        Infrastructure,
    )
    from eclypse.placement import Placement
    from eclypse.workflow.event import EclypseEvent


@metric.application
def soft_constraints(_: Application, pl: Placement, __: Infrastructure) -> int:
    """
    Count the number of chosen relaxed node in the placement.
    """
    rlx = pl.strategy.n_relaxed
    pl.strategy.n_relaxed = -1
    return rlx


@metric.application
def execution_time(_: Application, pl: Placement, __: Infrastructure) -> float:
    exec_time = pl.strategy.exec_time
    pl.strategy.exec_time = -1
    return exec_time


@metric.application
def inferences(_: Application, pl: Placement, __: Infrastructure) -> int:
    """
    Count the number of inferences made by the Prolog engine.
    """
    inferences = pl.strategy.inferences
    pl.strategy.inferences = -1
    return inferences


@metric.application
def is_placed(app: Application, pl: Placement, __: Infrastructure) -> bool:
    return len(pl.mapping) == len(app.nodes)


@metric.simulation(activates_on=["enact", "stop"])
class SuccessRate:
    """
    Count the number of successful placements.
    """

    def __init__(self):
        self.success_count = 0
        self.failure_count = 0

    def __call__(self, event: EclypseEvent) -> float:
        if event.name == "enact":
            app = event.simulator.applications.get("museuMonitor")
            pl = event.simulator.placements.get("museuMonitor")
            if len(pl.mapping) == len(app.nodes):
                self.success_count += 1
            else:
                self.failure_count += 1

        elif event.name == "stop":
            total = self.success_count + self.failure_count
            return self.success_count / total if total > 0 else 0.0


def get_metrics() -> List[EclypseEvent]:
    return [
        soft_constraints,
        execution_time,
        is_placed,
        SuccessRate(),
    ]
