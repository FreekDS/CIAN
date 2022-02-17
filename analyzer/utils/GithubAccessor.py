import os
import functools
import requests
import json
from typing import Dict, Any
from analyzer.Repository.Repo import Repo
from analyzer.utils import merge_dicts


class GithubAccessorError(Exception):
    def __init__(self, text, code):
        super(GithubAccessorError, self).__init__(text)
        self.status_code = code

# TODO investigate caching


class GithubAccessor:

    TOKENS = None
    TOKEN_PTR = 0

    def __init__(self):
        self.initialize()
        self._url_base = 'https://api.github.com'

    @property
    def token(self):
        return self.TOKENS[self.TOKEN_PTR]

    @staticmethod
    def use_token(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            GithubAccessor.TOKEN_PTR += 1
            GithubAccessor.TOKEN_PTR %= len(GithubAccessor.TOKENS)
            return ret
        return wrapper

    @use_token
    def _make_header(self):
        return {
            'Authorization': f'token {self.token}'
        }

    @staticmethod
    def initialize():
        if GithubAccessor.initialized():
            return
        t_count = int(os.getenv('GH_TOKEN_COUNT', 0))
        GithubAccessor.TOKENS = list()
        for i in range(t_count):
            token = os.getenv(f'GH_TOKEN_{i+1}', None)
            if token:
                GithubAccessor.TOKENS.append(token)

    @staticmethod
    def initialized():
        if GithubAccessor.TOKENS:
            return len(GithubAccessor.TOKENS) >= 1
        return False

    def _make_request(self, *args: str, query: str = str()):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        response = requests.get(url, headers=self._make_header())
        if response.status_code == 200 or response.status_code == 201:
            # With pagination
            if 'next' in response.links.keys():
                result = response.json()
                while 'next' in response.links.keys():
                    url = response.links.get('next').get('url')
                    response = requests.get(url, headers=self._make_header())
                    if response.status_code not in [200, 201]:
                        raise GithubAccessorError(
                            f"Cannot perform GitHub request '{url}', got response {response.status_code}",
                            response.status_code
                        )
                    result = merge_dicts(result, response.json())
                return json.dumps(result)
            # No pagination, simply return the response text
            return response.text
        raise GithubAccessorError(
            f"Cannot perform GitHub request '{url}', got response {response.status_code}", response.status_code
        )

    def get_content(self, repo: Repo, path) -> Dict[str, Any] or None:
        if path.endswith('/'):
            path = path[:-1]
        try:
            data = self._make_request('repos', repo.path, 'contents', path)
            return json.loads(data)
        except GithubAccessorError as e:
            if e.status_code == 404:
                return None
            raise e

    def get_jobs(self, repo: Repo, run_id: int) -> Dict[str, Any]:
        try:
            data = self._make_request('repos', repo.path, 'actions', 'runs', str(run_id), 'jobs')
            return json.loads(data)
        except GithubAccessorError as e:
            if e.status_code == 404:
                return dict()
            raise e

    def get_job_log(self, repo: Repo, job_id: int) -> str:
        try:
            data = self._make_request('repos', repo.path, 'actions', 'jobs', str(job_id), 'logs')
            return data
        except GithubAccessorError:
            return str()

    def get_workflows(self, repo: Repo) -> Dict[str, Any]:
        data = self._make_request('repos', repo.path, 'actions', 'workflows')
        return json.loads(data)

    def get_workflow_runs(self, repo: Repo, query: str = str()) -> Dict[str, Any]:
        data = self._make_request('repos', repo.path, 'actions', 'runs', query=query)
        return json.loads(data)

    def get_workflow_run_timing(self, repo: Repo, run_id: int):
        data = self._make_request('repos', repo.path, 'actions', 'runs', str(run_id), 'timing')
        return json.loads(data)
