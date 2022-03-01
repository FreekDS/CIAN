from typing import List

from Builds import Build
from analyzer.AntiPatterns.AntiPattern import AntiPattern


# TODO: for now, only logs from pytest are collected!


class SkipFailingTests(AntiPattern):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'SkipFailingTests')
        self.builds = self.sort_by_number()

    @staticmethod
    def delta_runs(build1: Build, build2: Build):
        return int()

    @staticmethod
    def delta_breaks(build1: Build, build2: Build):
        return int()

    @staticmethod
    def delta_skipped(build1: Build, build2: Build):
        return int()

    def build_has_skipped(self, prev_build: Build, build: Build):
        first_check = self.delta_breaks(prev_build, build) < 0
        second_check = self.delta_runs(prev_build, build) < 0
        third_check = self.delta_skipped(prev_build, build) > 0
        return first_check and (second_check or third_check)

    def detect(self) -> dict:
        pass
