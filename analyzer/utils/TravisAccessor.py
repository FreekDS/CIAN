import math

import requests
import os
import json
from typing import Dict, Any, List

from aiohttp import ClientResponseError, TCPConnector, ClientSession

from analyzer.Repository import Repo
import asyncio


class TravisAccessorError(Exception):
    def __init__(self, msg, status_code):
        super(TravisAccessorError, self).__init__(msg)
        self.status_code = status_code


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
                "Could not initialize TravisAccessor, check whether env variable TRAVIS_CI exists", -1)

    @staticmethod
    def initialize():
        if not TravisAccessor.initialized():
            TravisAccessor.TOKEN = os.getenv('TRAVIS_CI')

    @staticmethod
    def initialized():
        return TravisAccessor.TOKEN is not None

    def make_url(self, *args, query):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = url + f'?{query}'
        return url

    def _make_request(self, *args: str, query: str = "") -> str:
        url = self.make_url(*args, query=query)
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            return response.text
        raise TravisAccessorError(f"Could not make request to '{url}', got response code '{response.status_code}'",
                                  response.status_code)

    async def _make_request_async(self, session, *args: str, query: str = "") -> str:
        url = self.make_url(*args, query=query)
        try:
            async with session.get(url) as response:
                resp = await response.read()
                await asyncio.sleep(0)
                if response.status == 404:
                    return str()
                return resp
        except ClientResponseError as e:
            if e.status == 404:
                return str()
        except asyncio.TimeoutError:
            print("Timeout with url", url)
            return str()

    def get_builds(self, repo: Repo) -> List[Dict[Any, Any]]:
        limit = 100.0
        repo_name = repo.path.replace('/', '%2F')
        first_response = self._make_request('repo', repo_name, 'builds', query=f"limit={int(limit)}")
        first_response = json.loads(first_response)
        builds = first_response.get('builds', [])

        pagination_info = first_response.get('@pagination', False)
        if not pagination_info or pagination_info.get('is_last') is True:
            return builds
        c = float(pagination_info.get('count', 0)) - len(builds)
        requests_to_perform = math.ceil(c / limit)

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._multi_collect_builds(requests_to_perform, repo_name, limit)
        )
        loop.run_until_complete(future)

        builds += future.result()
        return builds

    async def _multi_collect_builds(self, requests_to_perform, repo_name, limit):
        tasks = list()
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn, headers=self._headers) as session:
            for i in range(1, requests_to_perform+1):
                q = f"limit={int(limit)}&offset={int(i * limit)}"
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'repo', repo_name, 'builds', query=q)
                )
                tasks.append(task)
            resp = await asyncio.gather(*tasks)
        resp = [json.loads(r) for r in resp]
        builds = list()
        for r in resp:
            builds += r.get('builds', [])
        return builds

    def get_repo(self, repo: Repo):
        try:
            repo_name = repo.path.replace('/', '%2F')
            resp = self._make_request('repo', repo_name)
            return json.loads(resp)
        except TravisAccessorError as e:
            if e.status_code == 404:
                return dict()
            raise e

    def get_job(self, job_id) -> Dict[Any, Any]:
        try:
            response = self._make_request('job', str(job_id))
            return json.loads(response)
        except TravisAccessorError as err:
            if err.status_code == 404:
                return {}

    def get_job_log(self, job_id) -> str:
        try:
            response = self._make_request('job', str(job_id), 'log.txt')
            return response
        except TravisAccessorError as err:
            if err.status_code == 404:
                return ""

    def collect_logs(self, job_ids):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._multi_collect_logs(job_ids)
        )
        loop.run_until_complete(future)
        return future.result()

    async def _multi_collect_logs(self, job_ids):
        tasks = list()
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn, headers=self._headers) as session:
            for job_id in job_ids:
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'job', str(job_id), 'log.txt')
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        res = dict()
        for i, j_id in enumerate(job_ids):
            res[j_id] = json.loads(results[i])
        return res

    def collect_jobs(self, job_ids):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            self._multi_collect_jobs(job_ids)
        )
        loop.run_until_complete(future)
        return future.result()

    async def _multi_collect_jobs(self, job_ids):
        tasks = list()
        conn = TCPConnector(limit=20)
        async with ClientSession(connector=conn, headers=self._headers) as session:
            for job_id in job_ids:
                task = asyncio.ensure_future(
                    self._make_request_async(session, 'job', str(job_id))
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        res = dict()
        for i, j_id in enumerate(job_ids):
            res[j_id] = json.loads(results[i])
        return res
