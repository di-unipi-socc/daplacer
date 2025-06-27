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


def get_metrics() -> List[EclypseEvent]:
    return [
        soft_constraints,
        execution_time,
        is_placed,
    ]
