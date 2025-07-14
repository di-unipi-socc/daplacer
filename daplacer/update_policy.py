from __future__ import annotations

import random as rnd
from collections import defaultdict
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from networkx.classes.reportviews import (
        EdgeView,
        NodeView,
    )


class ChangePolicy:

    def __init__(self, seed: int, change_prob: float, fail_prob: float = 0.02):
        self.change_probability = change_prob
        self.fail_probability = fail_prob
        self.old_resources = defaultdict(lambda: None)
        self.rnd = rnd.Random(seed)

    def __call__(self, _: Union[NodeView, EdgeView]):
        pass

    def fail(self):
        return self.rnd.random() < self.fail_probability


class ChangeNodePolicy(ChangePolicy):

    def __call__(self, nodes: NodeView):
        for n, resources in nodes.data():
            to_assert = False
            if self.old_resources[n] is None:
                self.old_resources[n] = resources.copy()
            else:
                resources.update(self.old_resources[n])
            if self.fail():
                resources["Ram"] = 0
                resources["Storage"] = 0
                to_assert = True
            elif rnd.random() < self.change_probability:
                ram = self.old_resources[n]["Ram"]
                hdd = self.old_resources[n]["Storage"]
                resources["Ram"] = round(rnd.uniform(ram * 0.9, ram * 1.1), 2)
                resources["Storage"] = round(rnd.uniform(hdd * 0.8, hdd * 1.2), 2)
                to_assert = True

            resources["Assert"] = to_assert


class ChangeLinkPolicy(ChangePolicy):

    def __call__(self, links: EdgeView):
        for n1, n2, resources in links.data():
            to_assert = False
            if self.old_resources[(n1, n2)] is None:
                self.old_resources[(n1, n2)] = resources.copy()
            if self.fail():
                resources["latency"] = 1000
                resources["bandwidth"] = 0
                to_assert = True
            if rnd.random() < self.change_probability:
                latency = self.old_resources[(n1, n2)]["latency"]
                bandwidth = self.old_resources[(n1, n2)]["bandwidth"]
                resources["latency"] = round(
                    rnd.uniform(latency * 0.85, latency * 1.15), 2
                )
                resources["bandwidth"] = round(
                    rnd.uniform(bandwidth * 0.9, bandwidth * 1.1), 2
                )
                to_assert = True
            resources["Assert"] = to_assert


def get_policies(seed: int, change_prob: float):
    return (
        ChangeNodePolicy(seed=seed, change_prob=change_prob),
        ChangeLinkPolicy(seed=seed, change_prob=change_prob),
    )
