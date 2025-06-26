from typing import Any, Dict, Callable
from eclypse.graph import Infrastructure


def bwth_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    infrastructure.graph["bwTh"] = iattr["Threshold"]


def node_ci_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    nid = iattr["NodeId"]
    infrastructure.nodes[nid]["CarbonIntensity"] = iattr["CI"]


def node_cost_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    nid = iattr["NodeId"]
    infrastructure.nodes[nid]["Cost"] = iattr["Cost"]


def node_handler(infrastructure: Infrastructure, **nattr: Dict[str, Any]):
    node_id = nattr.pop("NodeId")
    infrastructure.add_node(node_id, **nattr)


def link_handler(infrastructure: Infrastructure, **lattr: Dict[str, Any]):
    src, tgt = lattr.pop("SourceId"), lattr.pop("TargetId")
    infrastructure.add_edge(src, tgt, **lattr)


def sensor_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    sensor_id = iattr["SensorId"]
    infrastructure.graph.setdefault("sensors", {})[sensor_id] = {
        "type": iattr["SensorType"],
        "data": iattr["Data"],
    }


def actuator_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    actuator_id = iattr["ActuatorId"]
    infrastructure.graph.setdefault("actuators", {})[actuator_id] = {
        "type": iattr["ActuatorType"],
    }


def data_binding_handler(infrastructure: Infrastructure, **iattr: Dict[str, Any]):
    bindings = infrastructure.graph.setdefault("dataBindings", [])
    bindings.append((iattr["ServiceId"], iattr["RequirementId"], iattr["ThingId"]))


def get_handlers() -> Dict[str, Callable]:
    return {
        "bwTh": bwth_handler,
        "nodeCI": node_ci_handler,
        "nodeCost": node_cost_handler,
        "node": node_handler,
        "link": link_handler,
        "sensor": sensor_handler,
        "actuator": actuator_handler,
        "dataBinding": data_binding_handler,
    }
