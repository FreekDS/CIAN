from typing import List

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build


class BrokenRelease(AntiPattern):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'BrokenRelease')

    def detect(self) -> dict:
        pass

