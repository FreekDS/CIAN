from typing import List

from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.Workflow import Build
from analyzer.utils.Command import Command


class GithubActionsCollector(Command):
    def __init__(self, repo: GithubRepo):
        super(GithubActionsCollector, self).__init__()
        self.repo = repo

    def execute(self, *args, **kwargs) -> List[Build] or None:
        self.repo.fetch_builtin_ci()
        return self.repo.builds if self.repo.builds else None
