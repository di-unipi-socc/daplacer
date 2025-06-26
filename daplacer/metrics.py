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
    from eclypse.workflow import EclypseEvent


@metric.application
def soft_constraints(_: Application, placement: Placement, __: Infrastructure) -> int:
    """
    Count the number of chosen relaxed node in the placement.
    """
    rlx = placement.strategy.n_relaxed
    placement.strategy.n_relaxed = -1
    return rlx


@metric.application
def execution_time(_: Application, placement: Placement, __: Infrastructure) -> float:
    exec_time = placement.strategy.exec_time
    placement.strategy.exec_time = -1
    return exec_time


def get_metrics() -> List[EclypseEvent]:
    return [soft_constraints, execution_time]
