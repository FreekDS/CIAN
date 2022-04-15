from analyzer.Repository.Repo import Repo
from .TravisCollector import TravisCollector
from .GithubActionsCollector import GithubActionsCollector
from analyzer.Builds import Build
from analyzer.Cacher.BuildCache import BuildCache
from typing import List


def collect_builds(repo: Repo, use_cache=True, create_cache=True, from_date=None) -> List[Build]:

    cache = BuildCache(repo.path)

    if cache.hit() and use_cache:
        return cache.restore(default=[])

    collectors = [
        GithubActionsCollector(repo, from_date=from_date),
        TravisCollector(repo)
    ]

    builds = []

    for c in collectors:
        builds += c.execute()

    if create_cache:
        cache.create(builds)

    return builds
