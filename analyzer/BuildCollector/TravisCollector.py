import json
import os
import requests

from typing import List
from collections import defaultdict

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command
from analyzer.config import TRAVIS_CI
from analyzer.ResultsCollector import collect_test_results


class TravisCollector(Command):

    def __init__(self, repo: Repo):
        super().__init__()
        self.repo: Repo = repo
        # TODO: separate travis accessor functions/headers in separate class
        self.headers = {
            'Authorization': f'token {os.getenv("TRAVIS_CI")}',
            'Travis-API-Version': '3',
            'User-Agent': 'Git-Ci-Analyzer/v1.0'
        }

    def get_job(self, job_id):
        url = f'https://api.travis-ci.com/job/{job_id}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        return None

    def get_job_log(self, job_id):
        url = f'https://api.travis-ci.com/job/{job_id}/log.txt'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = str(response.text)
            return data
        return str()

    def get_test_results(self, raw_build):
        test_results = defaultdict(list)
        for job in raw_build.get('jobs', []):
            raw_job = self.get_job(job.get('id'))
            if not raw_job:
                continue
            job_name = raw_job.get('name')
            log = self.get_job_log(job.get('id'))
            tests = collect_test_results(log)
            if tests:
                test_results[job_name].append(tests)
        return dict(test_results)

    def execute(self, *args, **kwargs) -> List[Build]:
        url = 'https://api.travis-ci.com/repo/' + self.repo.path.replace('/', '%2F') + '/builds'
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            data = json.loads(req.text)
            raw_builds = data.get('builds')
            builds = list()
            for raw_build in raw_builds:
                build = Build.from_dict(raw_build, [('finished_at', 'ended_at')])
                build.created_by = build.created_by.get('login')
                build.branch = build.branch.get('name')
                build.used_tool = TRAVIS_CI
                build.test_results = self.get_test_results(raw_build)
                builds.append(build)
            return builds
        return []
