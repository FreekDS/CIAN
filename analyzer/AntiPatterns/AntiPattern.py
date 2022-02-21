from typing import List
from analyzer.Builds.Build import Build
from abc import ABC, abstractmethod
from collections import defaultdict


class AntiPattern(ABC):
    def __init__(self, builds: List[Build], name=''):
        self.builds = self.sort_by_workflow(builds)
        self.name = name

    @staticmethod
    def sort_by_workflow(builds):
        per_workflow = defaultdict(list)
        for build in builds:
            per_workflow[build.workflow].append(build)
        return per_workflow

    @abstractmethod
    def detect(self):
        raise NotImplementedError()

