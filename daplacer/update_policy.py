from __future__ import annotations

import random as rnd
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from networkx.classes.reportviews import (
        EdgeView,
        NodeView,
    )


class ChangePolicy:

    def __init__(self, seed: int, change_prob: float, fail_prob: float = 0.01):
        self.change_probability = change_prob
        self.fail_probability = fail_prob
        self.old_resources = defaultdict(lambda: None)
        self.rnd = rnd.Random(seed)

    def __call__(self, components):
        pass

    def fail(self):
        return self.rnd.random() < self.fail_probability


class ChangeNodePolicy(ChangePolicy):

    def __call__(self, nodes: NodeView):
        for n, resources in nodes.data(data=True):
            if self.old_resources[n] is None:
                self.old_resources[n] = resources.copy()
            else:
                resources.update(self.old_resources[n])
            if self.fail():
                resources["Ram"] = 0
                resources["Storage"] = 0
            elif rnd.random() < self.change_probability:
                ram = self.old_resources[n]["Ram"]  # resources["Ram"]
                hdd = self.old_resources[n]["Storage"]  # resources["Storage"]
                resources["Ram"] = round(rnd.uniform(ram // 10, ram * 1.1), 2)
                resources["Storage"] = round(rnd.uniform(hdd // 10, hdd * 1.2), 2)


class ChangeLinkPolicy(ChangePolicy):

    def __call__(self, links: EdgeView):
        for n1, n2, resources in links.data():
            if self.old_resources[(n1, n2)] is None:
                self.old_resources[(n1, n2)] = resources.copy()
            # if self.fail():
            #     resources["latency"] = 1000
            #     resources["bandwidth"] = 0
            if rnd.random() < self.change_probability:
                latency = self.old_resources[(n1, n2)][
                    "latency"
                ]  # resources["latency"]
                bandwidth = self.old_resources[(n1, n2)][
                    "bandwidth"
                ]  # resources["bandwidth"]
                resources["latency"] = round(
                    rnd.uniform(latency // 2, latency * 1.5), 2
                )
                resources["bandwidth"] = round(
                    rnd.uniform(bandwidth // 2, bandwidth * 1.1), 2
                )


def get_policies(seed: int, change_prob: float):
    # return (
    #     ChangeNodePolicy(seed=seed, change_prob=change_prob),
    #     ChangeLinkPolicy(seed=seed, change_prob=change_prob),
    # )
    return None, None
