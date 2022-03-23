import os
import functools
import requests
import json
import math
from typing import Dict, Any
from analyzer.Repository.Repo import Repo
from analyzer.utils import merge_dicts
import asyncio
from aiohttp import ClientSession, ClientResponseError


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

    def url_request(self, url, unfold_pagination=True):
        response = requests.get(url, headers=self._make_header())
        if response.status_code == 200 or response.status_code == 201:
            # With pagination
            if 'next' in response.links.keys() and unfold_pagination:
                result = response.json()
                while 'next' in response.links.keys():
                    url = response.links.get('next').get('url')
                    response = requests.get(url, headers=self._make_header())
                    if response.status_code not in [200, 201, 502]:
                        raise GithubAccessorError(
                            f"Cannot perform GitHub request '{url}', got response {response.status_code}",
                            response.status_code
                        )
                    elif response.status_code == 502:
                        print("Bad gateway on ", url, "Finishing earlier....", end='')
                        return json.dumps(result)

                    result = merge_dicts(result, response.json())
                return json.dumps(result)
            # No pagination, simply return the response text
            return response.text
        raise GithubAccessorError(
            f"Cannot perform GitHub request '{url}', got response {response.status_code}", response.status_code
        )

    def _make_request(self, *args: str, query: str = str(), unfold_pagination=True):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        return self.url_request(url, unfold_pagination=unfold_pagination)

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

    def get_workflow_runs(self, repo: Repo, start_date=None, query: str = str()) -> Dict[str, Any]:
        """
        First get total count (1 sync call), also get first 100 runs
        while count < total_count
            get 10 pages with 100 results (10 async calls)
            wait for 10 th page, and get latest date
                construct new calls
        """
        if query:
            query += '&'
        if start_date:
            query += f'>={start_date}&'
        query += 'per_page=100'
        first_response = json.loads(self._make_request('repos', repo.path, 'actions', 'runs', query=query))
        total_count = int(first_response.get('total_count', 0))
        runs_data = first_response.get('workflow_runs')

        total_requests_to_perform = max(0, math.ceil((total_count - len(runs_data)) / 100.0))
        if total_requests_to_perform == 0:
            return {
                'total_count': total_count,
                'workflow_runs': runs_data
            }

        last_wf = runs_data[-1]
        last_created = last_wf.get('run_started_at')

        run_batches = math.ceil(total_requests_to_perform / 10.0)   # 10 pages == 1000 builds
        for _ in range(run_batches):
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(
                self._workflow_run_batch(from_date=start_date, to_date=last_created, repo_path=repo.path)
            )
            loop.run_until_complete(future)
            new_runs = future.result()  # TODO check if order is preserved, important for next date

            last_wf = new_runs[-1]
            last_created = last_wf.get('run_started_at')

            runs_data += new_runs

        # Todo Remove possible duplicates?

        return {
            'total_count': total_count,
            'workflow_runs': runs_data
        }

    async def _workflow_run_batch(self, from_date, to_date, repo_path):

        tasks = []
        date_range = f"{from_date}..{to_date}"
        async with ClientSession(headers=self._make_header()) as session:
            for i in range(10):
                page = i + 1
                query = f"?created={date_range}&per_page=100&page={page}"
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'repos', repo_path, 'actions', 'runs', query=query)
                )
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

        runs = list()
        for r in responses:
            runs += r.get('workflow_runs', [])
        return runs

    async def _make_request_async(self, session, *args: str, query: str = str()):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        try:
            async with session.get(url, async_timeout=15) as response:
                resp = await response.read()
        except ClientResponseError as e:
            print("Client error", e.status)
            return {}
        except asyncio.TimeoutError:
            print("Timeout")
            return {}
        return json.loads(resp)

    def get_workflow_run_timing(self, repo: Repo, run_id: int):
        data = self._make_request('repos', repo.path, 'actions', 'runs', str(run_id), 'timing')
        return json.loads(data)

    def get_last_commit(self, repo):
        data = self._make_request('repos', repo.path, 'commits', query='per_page=1&page=1', unfold_pagination=False)
        data = json.loads(data)
        if data:
            return data[0]
        else:
            return dict()

    def get_branches_with_latest_commit(self, repo):
        branch_data = self._make_request('repos', repo.path, 'branches')
        branch_data = json.loads(branch_data)
        data = list()
        for branch in branch_data:
            commit_url = branch.get('commit', {}).get('url', None)
            if not commit_url:
                continue
            commit_data = self.url_request(commit_url)
            branch['commit'] = json.loads(commit_data)
            data.append(branch)
        return data

    def get_closed_prs(self, repo, base_branch=None, head_branch=None):
        query = 'state=closed'
        if base_branch:
            query += f'&base={base_branch}'
        if head_branch:
            query += f'&head={head_branch}'
        data = self._make_request('repos', repo.path, 'pulls', query=query)
        return json.loads(data)

    def is_pr_merged(self, repo, pull_request_nr):
        """
        Merged pull requests get response 204, if not merged, status 404 is returned
        :param repo: repository object
        :param pull_request_nr: number of the pull request
        :return: True if the pull request is merged
        :raises: GithubAccessorError if the status is not 204 or 404
        """
        try:
            _ = self._make_request('repos', repo.path, 'pulls', str(pull_request_nr), 'merge')
            return False
        except GithubAccessorError as e:
            if e.status_code == 204:
                return True
            elif e.status_code == 404:
                return False
            else:
                raise e
