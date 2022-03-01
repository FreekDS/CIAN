from typing import List
from analyzer.Builds.Build import Build
from abc import ABC, abstractmethod
from collections import defaultdict


class AntiPattern(ABC):
    def __init__(self, builds: List[Build], name=''):
        self.builds = self.sort_by_workflow(builds)
        self.name = name

    @staticmethod
    def sort_by_workflow(builds) -> dict:
        per_workflow = defaultdict(list)
        for build in builds:
            per_workflow[build.workflow].append(build)
        return dict(per_workflow)

    @abstractmethod
    def detect(self) -> dict:
        raise NotImplementedError()

    def _sort_fn(self, fn):
        sorted_dict = dict()
        for wf, builds in self.builds.items():
            builds.sort(key=fn)
            sorted_dict[wf] = builds
        return sorted_dict

    def sort_chronologically(self):
        return self._sort_fn(lambda build: build.start_date)

    def sort_by_number(self):
        return self._sort_fn(lambda build: build.number)
