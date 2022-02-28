from typing import List

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build


class BrokenRelease(AntiPattern):

    RELEASE_NAMES = ["main", "master"]

    def __init__(self, builds: List[Build], custom_release_branches: List[str] or None=None):
        super().__init__(builds, 'BrokenRelease')
        self.builds = self.sort_chronologically()
        if custom_release_branches:
            self.custom_branches = custom_release_branches
        else:
            self.custom_branches = []

    def get_release_branch_builds(self):
        filtered_builds = {}
        for wf, builds in self.builds.items():
            filtered = list(
                filter(
                    lambda build: build.branch in self.RELEASE_NAMES + self.custom_branches,
                    builds
                )
            )
            filtered_builds[wf] = filtered
        return filtered_builds

    @staticmethod
    def get_failing(release_builds):
        failing_builds = {}
        for wf, builds in release_builds:
            filtered = list(
                filter(
                    lambda build: build.state == 'failure',
                    builds
                )
            )
            failing_builds[wf] = filtered
        return failing_builds

    def detect(self) -> dict:
        pass

