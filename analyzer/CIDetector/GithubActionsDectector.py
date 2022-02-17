from analyzer.utils.Command import Command
from analyzer.config import GH_ACTIONS
from analyzer.Repository.Repo import Repo
from typing import Union


class GithubActionsDetector(Command):
    def execute(self, repo: Repo) -> Union[None or str]:
        if repo.repo_type == 'github':
            if repo.path_exists('.github/workflows'):
                if not repo.dir_empty('.github/workflows'):
                    return GH_ACTIONS
        return None
