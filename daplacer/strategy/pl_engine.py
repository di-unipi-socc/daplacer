import time
from typing import Any, Dict, Optional, Tuple

from swiplserver import (
    PrologThread,
)

from daplacer.utils import (
    PL_QUERY,
    parse_prolog,
    timed_async_query,
    timed_query,
)


def pl_process(
    prolog: PrologThread,
    app_name: str,
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
    exec_time = timeout if r is None else end_time if r == False else r["Time"]
    relaxed = -1

    if mapping:
        relaxed = sum(1 for _, (_, m) in mapping if m == "hard")
        mapping = {s: n for s, (n, _) in mapping}
        # str_pl = (
        #     "[" + ", ".join(["({}, {})".format(s, n) for s, n in mapping.items()]) + "]"
        # )
        # print(f"Assert PL mapping: {str_pl}")
    else:
        timed_query(prolog, query="retractall(deployment(_,_,_,_))")

    return mapping, relaxed, exec_time
