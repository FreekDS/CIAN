from typing import List

from Builds import Build
from analyzer.AntiPatterns.AntiPattern import AntiPattern


class SkipFailingTests(AntiPattern):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'SkipFailingTests')

    def detect(self) -> dict:
        pass
