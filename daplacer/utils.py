from __future__ import annotations

from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import numpy as np
from kubernetes.config import load_incluster_config, load_kube_config
from kubernetes.client import CoreV1Api
from swiplserver import (
    PrologQueryTimeoutError,
    PrologResultNotAvailableError,
    PrologThread,
    is_prolog_atom,
    is_prolog_functor,
    is_prolog_list,
    prolog_args,
)

""" ------------ """
NUM_NODES = 4
SEED = 42
USE_DOCKER = True
""" ------------ """

SCHEDULER_NAME = "daplacer-scheduler"
POD_NAME = "{}-deployment"
CONTAINER_NAME = "{}-container"
SLEEP_TIME = 2

ROOT_DIR = Path(__file__).parent
INFRS_DIR = ROOT_DIR / "infrastructures"
APPS_DIR = ROOT_DIR / "applications"
MANIFESTS_DIR = ROOT_DIR / "manifests"
PL_STRATEGY_DIR = ROOT_DIR / "reasoner"

DAP_FILE = PL_STRATEGY_DIR / "daplacer.pl"
PL_ALL_FILE = PL_STRATEGY_DIR / "placer-all.pl"
PL_RELAXED_FILE = PL_STRATEGY_DIR / "placer-relaxed.pl"

RELAXED_BIND = "relaxed"
APP_NAME = "museuMonitor"
PL_QUERY = f"dap({APP_NAME}, Placement, Routes, Inferences, Time)"

APP_FILE = APPS_DIR / f"{APP_NAME}.pl"
INFR_NAME = "infr{nodes}-{seed}.pl"

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

ASSERT = "assertz({})"
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

SW_CAPS = str(["python", "ubuntu", "mySQL"]).replace("'", "")
SEC_CAPS = str(["encryption", "auth"]).replace("'", "")

LAT_MIN, LAT_MAX = 5, 20
BW_MIN, BW_MAX = 100, 1000


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


def get_sec_reqs(
    data_ids: List[str], data_types: Dict[str, Dict[str, List[Any]]]
) -> List[str]:
    """Get the security requirements for a list of data IDs."""
    sec_reqs = set()
    for dt in data_ids:
        sec_reqs.update(data_types[dt]["SecReqs"])
    return list(sec_reqs)


def load_config():
    try:
        load_incluster_config()  # For in-cluster deployment
    except:
        load_kube_config()  # For local development (e.g., Minikube)


def load_api():
    load_config()
    return CoreV1Api()


def to_gib(kib_string):
    try:
        kib = int(kib_string.lower().replace("ki", ""))
        return round(kib / 1024 / 1024, 2)
    except:
        return 0


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
