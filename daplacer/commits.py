from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List,
)

from eclypse.workflow.event import event

from daplacer.utils import (
    ASSERT,
    DATA_TYPE,
    E2E,
    RETRACT,
    SERVICE,
    SERVICE_CI,
    SERVICE_COST,
    REQUIREMENT,
    timed_query,
)

if TYPE_CHECKING:
    from eclypse.graph import (
        Application,
        Infrastructure,
    )
    from eclypse.placement import Placement
    from eclypse.workflow.event import EclypseEvent
    from swiplserver import PrologThread


def get_commits(ticks: int, prolog: PrologThread) -> List[EclypseEvent]:
    tick_step = ticks // 6

    @event(activates_on=("tick", [tick_step]), event_type="application", verbose=True)
    def commit_1(app: Application, placement: Placement, __: Infrastructure):
        placement._to_reset = True
        app.logger.info("COMMIT1 - Adding location data type")
        app.graph["DataTypes"]["location"] = {
            "Size": 0.3,
            "SecReqs": ["encryption", "auth"],
        }

        timed_query(
            prolog,
            ASSERT.format(
                DATA_TYPE.format(
                    data_id="location", size=0.3, sec_reqs=["encryption", "auth"]
                )
            ),
        )

        app.logger.info("Adding localisator service")
        app.add_node(
            "localisator",
            Sw=["ubuntu"],
            Cpu=3,
            Ram=2,
            Storage=32,
            MigrationCost=20,
            DataIds=["location"],
            Sec=["encryption", "auth"],
            MaxCost=4.5,
            MaxCI=0.2,
        )

        timed_query(
            prolog,
            ASSERT.format(
                SERVICE.format(
                    service_id="localisator",
                    sw=["ubuntu"],
                    cpu=3,
                    ram=2,
                    storage=32,
                    data_ids=["location"],
                    migration_cost=20,
                )
            ),
        )
        timed_query(
            prolog,
            ASSERT.format(SERVICE_COST.format(service_id="localisator", max_cost=4.5)),
        )
        timed_query(
            prolog,
            ASSERT.format(SERVICE_CI.format(service_id="localisator", max_ci=0.2)),
        )

        app.logger.info("Adding locStorage service")
        app.add_node(
            "locStorage",
            Sw=["mySQL", "ubuntu"],
            Cpu=3,
            Ram=3,
            Storage=64,
            MigrationCost=80,
            DataIds=["location"],
            Sec=["encryption", "auth"],
            MaxCost=4,
            MaxCI=0.3,
        )

        timed_query(
            prolog,
            ASSERT.format(
                SERVICE.format(
                    service_id="locStorage",
                    sw=["mySQL", "ubuntu"],
                    cpu=3,
                    ram=3,
                    storage=64,
                    data_ids=["location"],
                    migration_cost=80,
                )
            ),
        )
        timed_query(
            prolog,
            ASSERT.format(SERVICE_COST.format(service_id="locStorage", max_cost=4)),
        )
        timed_query(
            prolog,
            ASSERT.format(SERVICE_CI.format(service_id="locStorage", max_ci=0.3)),
        )

        app.logger.info("Adding rLoc requirement")
        app.graph["Requirements"]["rLoc"] = {
            "Type": "location",
            "DataIds": ["location"],
        }
        timed_query(
            prolog,
            ASSERT.format(
                REQUIREMENT.format(
                    req_id="rLoc", thg_type="location", data_ids=["location"]
                )
            ),
        )

        app.logger.info("Adding e2e interactions")
        app.graph["e2e"] = {
            ("rLoc", "locStorage"): {"latency": 30, "DataRates": [("location", 40)]},
            ("locStorage", "localisator"): {
                "latency": 30,
                "DataRates": [("location", 40)],
            },
        }

        timed_query(
            prolog,
            ASSERT.format(
                E2E.format(
                    source_id="rLoc",
                    target_id="locStorage",
                    latency=30,
                    data_rates=[("location", 40)],
                )
            ),
        )

    @event(
        activates_on=("tick", [tick_step * 2]), event_type="application", verbose=True
    )
    def commit_2(app: Application, placement: Placement, __: Infrastructure):
        placement._to_reset = True
        app.logger.info(
            "COMMIT2 - Removing localisator service and its e2e interactions"
        )

        app.remove_node("localisator")
        timed_query(prolog, RETRACT.format("service(localisator, _, _, _, _)"))

        app.graph["e2e"].pop(("locStorage", "localisator"), None)
        timed_query(prolog, RETRACT.format("e2e(locStorage, localisator, _, _)"))

    @event(
        activates_on=("tick", [tick_step * 3]), event_type="application", verbose=True
    )
    def commit_3(app: Application, placement: Placement, __: Infrastructure):
        placement._to_reset = True
        app.logger.info("COMMIT3 - Changing locStorage requirements")

        loc_storage = app.nodes["locStorage"]
        loc_storage["Ram"] = 4
        loc_storage["Storage"] = 128
        loc_storage["MigrationCost"] = 120

    @event(
        activates_on=("tick", [tick_step * 4]), event_type="application", verbose=True
    )
    def commit_4(app: Application, placement: Placement, __: Infrastructure):
        placement._to_reset = True
        app.logger.info("COMMIT4 - Changing e2e interaction parameters")

        app.graph["e2e"][("locStorage", "interface")] = {
            "latency": 50,
            "DataRates": [("location", 40)],
        }
        timed_query(prolog, RETRACT.format("e2e(locStorage, interface, _, _)"))
        timed_query(
            prolog,
            ASSERT.format(
                E2E.format(
                    source_id="locStorage",
                    target_id="interface",
                    latency=50,
                    data_rates=[("location", 40)],
                )
            ),
        )

        app.graph["e2e"][("locStorage", "controller")] = {
            "latency": 40,
            "DataRates": [("location", 40)],
        }

        timed_query(prolog, RETRACT.format("e2e(locStorage, controller, _, _)"))
        timed_query(
            prolog,
            ASSERT.format(
                E2E.format(
                    source_id="locStorage",
                    target_id="controller",
                    latency=40,
                    data_rates=[("location", 40)],
                )
            ),
        )

    @event(
        activates_on=("tick", [tick_step * 5]), event_type="application", verbose=True
    )
    def commit_5(app: Application, placement: Placement, __: Infrastructure):
        placement._to_reset = True
        app.logger.info("COMMIT5 - Changing e2e interaction parameters")
        app.graph["e2e"][("locStorage", "interface")] = {
            "latency": 30,
            "DataRates": [("location", 50)],
        }
        app.graph["e2e"][("locStorage", "controller")] = {
            "latency": 40,
            "DataRates": [("location", 60)],
        }

    @event(event_type="application", activates_on="tick", verbose=True)
    def invalidate_placement(
        app: Application, placement: Placement, __: Infrastructure
    ):
        placement._reset_mapping()

    return [commit_1, commit_2, commit_3, commit_4, commit_5, invalidate_placement]
