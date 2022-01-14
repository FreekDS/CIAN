from typing import List, AnyStr
from .TravisDetector import TravisDetector
from .GithubActionsDectector import GithubActionsDetector
from .CircleCIDetector import CircleCIDetector
from analyzer.Repository.Repo import Repo
from analyzer.Cacher.DetectorCache import DetectorCache


def detect_ci_tools(repo: Repo, use_cache=True, create_cache=True) -> List[AnyStr]:

    cache = DetectorCache(repo.name)

    if use_cache and cache.hit():
        return cache.restore(default=[])

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
        cache.create(tools)

    return tools
