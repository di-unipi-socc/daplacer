from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np

from swiplserver import (
    PrologQueryTimeoutError,
    PrologResultNotAvailableError,
    PrologThread,
    is_prolog_atom,
    is_prolog_functor,
    is_prolog_list,
    prolog_args,
)

ROOT_DIR = Path(__file__).parent
INFRS_DIR = ROOT_DIR / "infrastructures"
PL_STRATEGY_DIR = ROOT_DIR / "strategy" / "prolog"
DAP_FILE = PL_STRATEGY_DIR / "daplacer.pl"
PL_ALL_FILE = PL_STRATEGY_DIR / "placer-all.pl"
PL_RELAXED_FILE = PL_STRATEGY_DIR / "placer-relaxed.pl"

RELAXED_BIND = "relaxed"
APP_NAME = "museuMonitor"
PL_QUERY = f"dap({APP_NAME}, Placement, Routes, Inferences, Time)"

# Application templates
APPLICATION = "application({app_id}, {service_ids})"
SERVICE = "service({service_id}, {sw}, ({cpu}, {ram}, {storage}), {data_ids}, {migration_cost})"
SERVICE_COST = "serviceCost({service_id}, {max_cost})"
SERVICE_CI = "serviceCI({service_id}, {max_ci})"

DATA_TYPE = "dataType({data_id}, {size}, {sec_reqs})"
REQUIREMENT = "requirement({req_id}, {thg_type}, {data_ids})"
E2E = "e2e({source_id}, {target_id}, {latency}, {data_rates})"

# Infrastructure templates
NODE = "node({node_id}, {sw}, ({cpu}, {ram}, {storage}), {sec_caps}, {things})"
NODE_UNIT_COST = "nodeUnitCost({node_id}, {cpu_cost}, {ram_cost}, {storage_cost})"
NODE_CI = "nodeCI({node_id}, {ci})"
LINK = "link({u}, {v}, {latency}, {bandwidth})"

ASSERT = "assert({})"
RETRACT = "retractall({})"
CONSULT = "consult('{}')"

DYNAMICS = [
    "node/5",
    "link/4",
    "service/5",
    "dataType/3",
    "e2e/4",
    "serviceCost/2",
    "serviceCI/2",
    "requirement/3",
]


def parse_prolog(query):
    if is_prolog_list(query):
        ans = [parse_prolog(v) for v in query]
    elif is_prolog_functor(query):
        ans = tuple(parse_prolog(prolog_args(query)))
    elif is_prolog_atom(query):
        ans = query
    else:
        ans = query
    return ans


def consult(prolog: PrologThread, file: str):
    timed_query(prolog=prolog, query=CONSULT.format(file), clean=False)


def timed_async_query(
    prolog: PrologThread,
    query: str,
    timeout: Optional[int] = None,
    find_all: Optional[bool] = False,
):
    try:
        prolog.query_async(query, find_all=find_all)
        r = prolog.query_async_result(wait_timeout_seconds=timeout)
        if not find_all:
            prolog.cancel_query_async()
        r = r[0] if isinstance(r, list) else r
    except PrologResultNotAvailableError:
        print(f"Timeout: {query} took longer than {timeout} seconds.")
        prolog.cancel_query_async()
        r = None

    return r


def timed_query(
    prolog: PrologThread,
    query: str,
    timeout: Optional[int] = None,
    clean: bool = True,
):
    if clean:
        query = query.replace("'", "")
    try:
        r = prolog.query(query, query_timeout_seconds=timeout)
    except PrologQueryTimeoutError:
        print(f"Timeout: {query} took longer than {timeout} seconds.")
        r = None
    except Exception as e:
        print(f"Error executing query '{query}': {e}")
        r = None
    return r


def get_sec_reqs(
    data_ids: List[str], data_types: Dict[str, Dict[str, List[Any]]]
) -> List[str]:
    """Get the security requirements for a list of data IDs."""
    sec_reqs = set()
    for dt in data_ids:
        sec_reqs.update(data_types[dt]["SecReqs"])
    return list(sec_reqs)
