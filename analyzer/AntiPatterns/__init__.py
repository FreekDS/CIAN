from .SlowBuild import SlowBuild
from .LateMerging import LateMerging
from .BrokenRelease import BrokenRelease
from .SkipFailingTests import SkipFailingTests
from .AntiPattern import AntiPattern

from typing import List
from analyzer.Builds.Build import Build


def find_anti_patterns(builds: List[Build], branch_info: dict, default_branch, restriction=None):

    detectors: List[AntiPattern] = [
        SlowBuild(builds),
        LateMerging(builds, branch_info=branch_info),
        BrokenRelease(builds, default_branch=default_branch),
        SkipFailingTests(builds)
    ]

    result = dict()

    for detector in detectors:
        if restriction:
            if detector.name in restriction:
                result[detector.name] = detector.detect()
        else:
            result[detector.name] = detector.detect()

    return result
