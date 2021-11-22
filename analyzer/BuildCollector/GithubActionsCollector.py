from typing import List

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command


class GithubActionsCollector(Command):
    def __init__(self, repo: Repo):
        super(GithubActionsCollector, self).__init__()
        self.repo = repo

    def execute(self, *args, **kwargs) -> List[Build]:
        if self.repo.repo_type != 'github':
            return []
        self.repo.fetch_builtin_ci()
        return self.repo.builds if self.repo.builds else []
