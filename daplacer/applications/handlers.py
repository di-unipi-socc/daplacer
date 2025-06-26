from typing import (
    Any,
    Callable,
    Dict,
)

from eclypse.graph import Application

from daplacer.utils import get_sec_reqs


def application_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    application.name = attrs.pop("AppId")


def datatype_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    did = attrs["DataId"]
    application.graph.setdefault("DataTypes", {})[did] = {
        "Size": attrs["Size"],
        "SecReqs": attrs["SecReqs"],
    }


def service_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    sid = attrs.pop("ServiceId")
    data_ids = attrs.pop("DataIds")
    application.add_node(
        sid,
        Sw=attrs.pop("Sw"),
        Cpu=attrs.pop("Cpu"),
        Ram=attrs.pop("Ram"),
        Storage=attrs.pop("Storage"),
        DataIds=data_ids,
        Sec=get_sec_reqs(data_ids, application.graph.get("DataTypes")),
        MigrationCost=attrs.pop("MigrationCost"),
    )


def service_cost_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    sid = attrs["ServiceId"]
    application.nodes[sid]["MaxCost"] = attrs.pop("MaxCost")


def service_ci_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    sid = attrs["ServiceId"]
    application.nodes[sid]["MaxCI"] = attrs.pop("MaxCI")


def requirement_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    rid = attrs["ReqId"]
    application.graph.setdefault("Requirements", {})[rid] = {
        "Type": attrs["Type"],
        "DataIds": attrs["DataIds"],
    }


def e2e_handler(application: Application, **attrs: Dict[str, Any]) -> None:
    src, tgt = attrs.pop("SourceId"), attrs.pop("TargetId")
    application.graph.setdefault("e2e", {})[(src, tgt)] = attrs


def get_handlers() -> Dict[str, Callable]:
    return {
        "application": application_handler,
        "dataType": datatype_handler,
        "service": service_handler,
        "serviceCost": service_cost_handler,
        "serviceCI": service_ci_handler,
        "requirement": requirement_handler,
        "e2e": e2e_handler,
    }
