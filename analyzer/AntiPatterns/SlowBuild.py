from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List


class SlowBuild(AntiPattern):
    def __init__(self, builds: List[Build]):
        super().__init__(builds)

    def detect(self):
        pass
