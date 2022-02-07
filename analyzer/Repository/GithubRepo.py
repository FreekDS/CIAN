import datetime
import os
import json
import requests

from github import Github
from github import Repository as GH_Repository
from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.config import GH_ACTIONS
from analyzer.ResultsCollector import collect_test_results
from analyzer.utils.GithubAccessor import GithubAccessor
from collections import defaultdict


class GithubRepo(Repo):
    _githubObject = Github()

    @staticmethod
    def init_github_token(token):
        GithubRepo._githubObject = Github(login_or_token=token)

    def __init__(self, path):
        super().__init__(path, repo_type='github')
        self._fetched = False
        self._gh_access = GithubAccessor()
        self._repo: GH_Repository = self._githubObject.get_repo(path)
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

    def _get_jobs(self, wf_run):
        response = requests.get(wf_run.jobs_url, headers=self._headers)

        if response.status_code == 200:
            jobs_data = json.loads(response.text)
            return jobs_data.get('jobs', [])
        else:
            return []

    def _get_log_file(self, job_id):
        owner = self._repo.owner.login
        repo = self._repo.name
        request_url = f'{self._base_url}/repos/{owner}/{repo}/actions/jobs/{job_id}/logs'
        response = requests.get(request_url, headers=self._headers)
        if response.status_code == 200:
            return str(response.text)
        else:
            return str()
