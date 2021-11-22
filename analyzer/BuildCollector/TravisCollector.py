import json
from typing import List

import requests

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command
import os


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
                build.used_tool = 'TravisCI'
                builds.append(build)
            return builds
        return []
