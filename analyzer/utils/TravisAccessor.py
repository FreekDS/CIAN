import requests
import os
import json
from typing import Dict, Any, List
from analyzer.Repository import Repo


class TravisAccessorError(Exception):
    pass


class TravisAccessor:
    TOKEN = None

    def __init__(self):
        TravisAccessor.initialize()
        if self.initialized():
            self._headers = {
                'Authorization': f'token {TravisAccessor.TOKEN}',
                'Travis-API-Version': '3',
                'User-Agent': 'Git-Ci-Analyzer/v1.0'
            }
            self._url_base = 'https://api.travis-ci.com'
        else:
            raise TravisAccessorError(
                "Could not initialize TravisAccessor, check whether env variable TRAVIS_CI exists")

    @staticmethod
    def initialize():
        if not TravisAccessor.initialized():
            TravisAccessor.TOKEN = os.getenv('TRAVIS_CI')

    @staticmethod
    def initialized():
        return TravisAccessor.TOKEN is not None

    def _make_request(self, *args: str, query: str = "") -> str:
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = url + f'?{query}'
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            return response.text
        raise TravisAccessorError(f"Could not make request to '{url}', got response code '{response.status_code}'")

    def get_builds(self, repo: Repo) -> List[Dict[Any, Any]]:
        repo_name = repo.path.replace('/', '%2F')
        response = self._make_request('repo', repo_name, 'builds')
        response = json.loads(response)
        return response.get('builds')

    def get_repo(self, repo: Repo):
        repo_name = repo.path.replace('/', '%2F')
        resp = self._make_request('repo', repo_name)
        return json.loads(resp)

    def get_job(self, job_id) -> Dict[Any, Any]:
        response = self._make_request('job', str(job_id))
        return json.loads(response)

    def get_job_log(self, job_id) -> str:
        response = self._make_request('job', str(job_id), 'log.txt')
        return response
