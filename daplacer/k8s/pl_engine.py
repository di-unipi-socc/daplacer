from __future__ import annotations

import time
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Tuple,
)

from daplacer.utils import (
    PL_QUERY,
    RELAXED_BIND,
    parse_prolog,
    timed_async_query,
    timed_query,
)

if TYPE_CHECKING:
    from swiplserver import PrologThread


def pl_process(
    app_name: str,
    prolog: PrologThread,
    timeout: Optional[int] = None,
) -> Tuple[Optional[Dict[str, Any]], int, float]:
    start_time = time.time()

    r = timed_async_query(
        prolog,
        query=PL_QUERY.format(app=app_name),
        timeout=timeout,
    )
    end_time = time.time() - start_time
    mapping = parse_prolog(r["Placement"]) if r else {}
    exec_time = timeout if r is None else end_time if r is False else r["Time"]
    inferences = r["Inferences"] if r else 0

    if mapping:
        mapping = {s: n for s, (n, _) in mapping}
        str_pl = "[" + ", ".join(f"({s}, {n})" for s, n in mapping.items()) + "]"
        print(f"Assert PL mapping: {str_pl}")
    else:
        print("No mapping found, asserting empty placement.")
        timed_query(prolog, "retractall(deployment(_,_,_,_))")

    return mapping, exec_time, inferences
