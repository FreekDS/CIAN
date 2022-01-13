from analyzer.Repository.Repo import Repo
from .TravisCollector import TravisCollector
from .GithubActionsCollector import GithubActionsCollector
from analyzer.Builds import Build
from typing import List

import analyzer.Cacher.BuildCacher as Cache


def collect_builds(repo: Repo, use_cache=True, create_cache=True) -> List[Build]:

    if Cache.hit() and use_cache:
        return Cache.restore_cache()

    collectors = [
        GithubActionsCollector(repo),
        TravisCollector(repo)
    ]

    builds = []

    for c in collectors:
        builds += c.execute()

    if create_cache:
        Cache.create_cache(builds)

    return builds
