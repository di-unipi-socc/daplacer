import time
from pathlib import Path
from typing import (
    Any,
    Dict,
)

import ray
from eclypse.simulation import (
    Simulation,
    SimulationConfig,
)
from eclypse.utils.constants import DEFAULT_SIM_PATH
from ray import (
    train,
    tune,
)
from swiplserver import PrologMQI

from daplacer.applications.parser import get_application
from daplacer.assets import (
    edge_assets,
    get_default_path_aggregators,
    node_assets,
)
from daplacer.builder import generate_infrastructures
from daplacer.commits import get_commits
from daplacer.infrastructures.parser import get_infrastructure
from daplacer.metrics import get_metrics
from daplacer.search_space import (
    NODES,
    SEEDS,
    search_space,
)
from daplacer.strategy import DAPlacerStrategy
from daplacer.update_policy import get_policies


def daplacer_grid(config: Dict[str, Any], with_ray: bool = True):
    if with_ray:
        stg = train.get_context().get_storage()
        path = (
            Path(stg.storage_fs_path)
            / stg.experiment_dir_name
            / str(stg.trial_dir_name)
            / "output"
        )
    else:
        path = DEFAULT_SIM_PATH / "daplacer"

    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog:
            sim_config = SimulationConfig(
                seed=config["seed"],
                max_ticks=config["max_ticks"],
                tick_every_ms="auto",
                include_default_callbacks=False,
                events=get_metrics() + get_commits(config["max_ticks"], prolog),
                path=path,
                log_level="TRACE",
                log_to_file=True,
            )

            app = get_application(
                application_id=config["application_id"],
                node_assets=node_assets,
                edge_assets=edge_assets,
                seed=config["seed"],
            )

            node_update_policy, edge_update_policy = get_policies(
                seed=config["seed"], change_prob=config["change_prob"]
            )

            infr = get_infrastructure(
                n=config["nodes"],
                seed=config["seed"],
                topology=config["topology"],
                node_update_policy=node_update_policy,
                edge_update_policy=edge_update_policy,
                node_assets=node_assets,
                edge_assets=edge_assets,
                path_assets_aggregators=get_default_path_aggregators(),
            )

            sim = Simulation(infrastructure=infr, simulation_config=sim_config)
            sim.register(
                application=app,
                placement_strategy=DAPlacerStrategy(
                    prolog=prolog, timeout=config["timeout"]
                ),
            )

            sim.start()
            sim.wait()


if __name__ == "__main__":
    config_example = {
        "application_id": "museuMonitor",
        "nodes": 32,
        "seed": 3997,
        "topology": "BA",
        "timeout": 100,
        "max_ticks": 20,
        "change_prob": 0.1,
    }

    # generate all the infrastructures and corresponding Prolog knowledge bases
    generate_infrastructures(nodes=NODES, seeds=SEEDS)
    # Example usage of the daplacer_grid function
    daplacer_grid(config_example, with_ray=False)
    # ray.init(address="auto")

    # start_time = time()
    # run_config = train.RunConfig(storage_path=(DEFAULT_SIM_PATH).resolve())
    # tuner = tune.Tuner(daplacer_grid, param_space=search_space, run_config=run_config)

    # # tuner = tune.Tuner.restore(
    # #     "/home/massa/eclypse-sim/edgewise_grid_2025-02-20_15-07-31",
    # #     trainable=tune.with_resources(edgewise_grid, {"cpu": 2}),
    # #     param_space=search_space,
    # #     restart_errored=True,
    # # )

    # tuner.fit()
    # print("Elapsed time: ", time() - start_time)
