import os

from analyzer.Repository.Repo import Repo
from analyzer.utils.GithubAccessor import GithubAccessor


class GithubRepo(Repo):

    def __init__(self, path):
        super().__init__(path, repo_type='github')
        self._gh_access = GithubAccessor()
        self._base_url = 'https://api.github.com'
        self._headers = {'Authorization': f'token {os.getenv("GH_TOKEN")}'}

    def path_exists(self, path) -> bool:
        return self._gh_access.get_content(self, path) is not None

    def dir_empty(self, path) -> bool:
        if not self.path_exists(path):
            return False
        content = self._gh_access.get_content(self, path)
        if isinstance(content, list):
            return len(content) == 0
        # is not directory, return True
        return True
