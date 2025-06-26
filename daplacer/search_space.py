from ray.tune import grid_search

NODES = [16, 32, 64, 128, 256, 512]
SEEDS = [3997, 151195, 300425]

search_space = {
    "timeout": 100,
    "max_ticks": 60,
    "application_id": "museuMonitor",
    "seed": grid_search(SEEDS),
    "nodes": grid_search(NODES),
    "topology": "BA",
    "change_prob": grid_search([0.1, 0.2, 0.4, 0.5]),
}

__all__ = ["search_space", NODES, SEEDS]
