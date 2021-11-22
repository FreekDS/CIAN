from analyzer.Repository.Repo import Repo
from .TravisCollector import TravisCollector
from .GithubActionsCollector import GithubActionsCollector
from analyzer.Builds import Build
from typing import List


def collect_builds(repo: Repo) -> List[Build]:

    collectors = [
        GithubActionsCollector(repo),
        TravisCollector(repo)
    ]

    builds = []

    for c in collectors:
        builds += c.execute()

    return builds
