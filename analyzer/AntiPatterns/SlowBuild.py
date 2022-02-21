import datetime

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List

# TODO: add threshold parameters, when is a build slow?


class SlowBuild(AntiPattern):
    def __init__(self, builds: List[Build]):
        super().__init__(builds)
        self.builds = self.sort_chronologically()

    def average_duration_weekly(self):
        pass

    def sort_chronologically(self):
        sorted_dict = dict()
        for wf, builds in self.builds.items():
            builds.sort(key=lambda build: build.start_date)
            sorted_dict[wf] = builds
        return sorted_dict

    def detect(self):
        pass
