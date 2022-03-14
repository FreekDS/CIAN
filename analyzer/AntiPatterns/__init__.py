from .SlowBuild import SlowBuild
from .LateMerging import LateMerging
from .BrokenRelease import BrokenRelease
from .SkipFailingTests import SkipFailingTests
from .AntiPattern import AntiPattern

from typing import List
from analyzer.Builds.Build import Build


def find_anti_patterns(builds: List[Build], branch_info: dict):

    detectors: List[AntiPattern] = [
        SlowBuild(builds),
        LateMerging(builds, branch_info=branch_info),
        BrokenRelease(builds),
        SkipFailingTests(builds)
    ]

    result = dict()

    for detector in detectors:
        result[detector.name] = detector.detect()

    return result
