import os
import functools
import requests
import json
import math
from typing import Dict, Any, List
from analyzer.Repository.Repo import Repo
from analyzer.utils import merge_dicts, format_date
import asyncio
from aiohttp import ClientSession, ClientResponseError, TCPConnector


class GithubAccessorError(Exception):
    def __init__(self, text, code):
        super(GithubAccessorError, self).__init__(text)
        self.status_code = code


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
            'Authorization': f'token {self.token}',
            'User-Agent': 'FreekDS/git-ci-analyzer'
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
        elif response.status_code == 502:
            print(f"Cannot perform GitHub request '{url}', got response {response.status_code}, {response.content}")
            return "{}"
        raise GithubAccessorError(
            f"Cannot perform GitHub request '{url}', got response {response.status_code}, {response.content}",
            response.status_code
        )

    def _make_request(self, *args: str, query: str = str(), unfold_pagination=True):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        return self.url_request(url, unfold_pagination=unfold_pagination)

    def get_repo_info(self, repo: Repo):
        try:
            data = self._make_request('repos', repo.path)
            return json.loads(data)
        except GithubAccessorError as ge:
            print("Cannot fetch repo info, ", ge)
            return {}

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

    def batch_collect_jobs(self, repo: Repo, run_ids: List[int]):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._batch_collect_jobs(repo, run_ids)
        )
        loop.run_until_complete(future)
        return future.result()

    async def _batch_collect_jobs(self, repo: Repo, run_ids: List[int]):
        tasks = list()
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn) as session:
            for run_id in run_ids:
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'repos', repo.path, 'actions', 'runs', str(run_id), 'jobs')
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        return results

    def get_job_log(self, repo: Repo, job_id: int) -> str:
        try:
            data = self._make_request('repos', repo.path, 'actions', 'jobs', str(job_id), 'logs')
            return data
        except GithubAccessorError:
            return str()

    def batch_collect_job_logs(self, repo: Repo, job_ids: List[int]):
        if not job_ids:
            return {}
        log = self.get_job_log(repo, job_ids[0])
        if 'Must have admin rights to Repository' in log:
            print("Job logs are not available, admin rights are required")
            return {}
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._batch_collect_job_logs(repo, job_ids)
        )
        loop.run_until_complete(future)
        return future.result()

    async def _batch_collect_job_logs(self, repo: Repo, job_ids: List[int]):
        tasks = list()
        try:
            connector = TCPConnector(limit=20)
            async with ClientSession(connector=connector) as session:
                for job_id in job_ids:
                    task = asyncio.ensure_future(
                        self._make_request_async(
                            session, 'repos', repo.path, 'actions', 'jobs', str(job_id), 'logs',
                            as_text=True
                        )
                    )
                    tasks.append(task)
                results = await asyncio.gather(*tasks)
        except ClientResponseError:
            return {}
        result_dict = {}
        for i, log in enumerate(results):
            result_dict[job_ids[i]] = log
        return result_dict

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
            query += f'created=>={start_date}&'
        query += 'per_page=100'
        first_response = json.loads(
            self._make_request('repos', repo.path, 'actions', 'runs', query=query, unfold_pagination=False)
        )
        total_count = int(first_response.get('total_count', 0))
        runs_data = first_response.get('workflow_runs', [])

        total_requests_to_perform = max(0, math.ceil(float(total_count - len(runs_data)) / 100.0))
        if total_requests_to_perform == 0:
            return {
                'total_count': total_count,
                'workflow_runs': runs_data
            }

        def get_date(d):
            date = format_date(d)
            return date.strftime("%Y-%m-%d")

        last_wf = runs_data[-1]
        last_created = get_date(last_wf.get('run_started_at'))

        run_batches = math.ceil(total_requests_to_perform / 10.0)   # 10 pages == 1000 builds
        for _ in range(run_batches):
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(
                self._workflow_run_batch(from_date=start_date, to_date=last_created, repo_path=repo.path)
            )
            loop.run_until_complete(future)
            new_runs = future.result()

            if new_runs:
                last_wf = new_runs[-1]
                last_created = get_date(last_wf.get('run_started_at'))

                runs_data += new_runs

        seen = set()
        seen_add = seen.add
        runs_data = [x for x in runs_data if not (x.get('id') in seen or seen_add(x.get('id')))]

        runs_data.sort(key=lambda run: format_date(run.get('created_at')), reverse=True)

        return {
            'total_count': total_count,
            'workflow_runs': runs_data
        }

    async def _workflow_run_batch(self, from_date, to_date, repo_path):

        tasks = []
        date_range = f"{from_date}..{to_date}"
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn) as session:
            for i in range(10):
                page = i + 1
                query = f"per_page=100&page={page}&created={date_range}"
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'repos', repo_path, 'actions', 'runs', query=query)
                )
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

        runs = list()
        for r in responses:
            runs += r.get('workflow_runs', [])
        runs.sort(key=lambda run: format_date(run.get('created_at')), reverse=True)
        return runs

    async def _make_request_async(self, session, *args: str, query: str = str(), as_text=False):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        try:
            async with session.get(url, headers=self._make_header()) as response:
                resp = await response.read()
                await asyncio.sleep(0)
        except ClientResponseError as e:
            if e.status != 404:
                print("Client error", e.status)
            return {}
        except asyncio.TimeoutError:
            print("Timeout")
            return {}
        return json.loads(resp) if not as_text else resp.decode()

    def get_workflow_run_timing(self, repo: Repo, run_id: int):
        data = self._make_request('repos', repo.path, 'actions', 'runs', str(run_id), 'timing')
        return json.loads(data)

    def batch_collect_run_timing(self, repo: Repo, run_ids: List[int]):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._batch_collect_run_timing(repo, run_ids)
        )
        loop.run_until_complete(future)
        return future.result()

    async def _batch_collect_run_timing(self, repo: Repo, run_ids: List[int]):
        tasks = list()
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn) as session:
            for run_id in run_ids:
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'repos', repo.path, 'actions', 'runs', str(run_id), 'timing')
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        return results

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
