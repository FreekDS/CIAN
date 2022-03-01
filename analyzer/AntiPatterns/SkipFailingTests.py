from typing import List

from Builds import Build
from analyzer.AntiPatterns.AntiPattern import AntiPattern


# TODO: for now, only logs from pytest are collected!


class SkipFailingTests(AntiPattern):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'SkipFailingTests')

    def detect(self) -> dict:
        pass
