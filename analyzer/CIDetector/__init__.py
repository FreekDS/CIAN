from typing import List, AnyStr
from .TravisDetector import TravisDetector
from .GithubActionsDectector import GithubActionsDetector
from .CircleCIDetector import CircleCIDetector
from analyzer.Repository.Repo import Repo

import analyzer.Cacher.DetectorCache as Cache


def detect_ci_tools(repo: Repo, use_cache=True, create_cache=True) -> List[AnyStr]:

    if use_cache and Cache.hit():
        return Cache.restore_cache()

    detectors = [
        TravisDetector(),
        GithubActionsDetector(),
        CircleCIDetector()
    ]

    tools = []
    for detector in detectors:
        detected = detector.execute(repo)
        if detected:
            tools.append(detected)

    if create_cache:
        Cache.create_cache(tools)

    return tools
