from analyzer.utils.Command import Command
from analyzer.config import TRAVIS_CI
from analyzer.utils.TravisAccessor import TravisAccessor
from analyzer.Repository.Repo import Repo
from typing import Union


class TravisDetector(Command):
    def __init__(self):
        self.travis_access = TravisAccessor()

    def execute(self, repo: Repo) -> Union[None or str]:
        repo_data = self.travis_access.get_repo(repo)
        if repo_data.get('active', False) is True:
            return TRAVIS_CI
        return None
