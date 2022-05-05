from typing import List
from collections import defaultdict

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command
# from analyzer.utils import timing
from analyzer.utils.TravisAccessor import TravisAccessor, TravisAccessorError
from analyzer.config import TRAVIS_CI
from analyzer.ResultsCollector import collect_test_results


class TravisCollector(Command):

    def __init__(self, repo: Repo, from_date=None):
        super().__init__()
        self.repo: Repo = repo
        self.travis_access = TravisAccessor()
        self.from_date = from_date

    def get_test_results(self, raw_build):
        test_results = defaultdict(list)
        for job in raw_build.get('jobs', []):
            raw_job = self.travis_access.get_job(job.get('id'))
            if not raw_job:
                continue
            job_name = raw_job.get('name')
            log = self.travis_access.get_job_log(job.get('id'))
            tests = collect_test_results(log)
            if tests:
                test_results[job_name].append(tests)
        return dict(test_results)

    # @timing
    def execute(self, *args, **kwargs) -> List[Build]:
        try:
            raw_builds = self.travis_access.get_builds(self.repo)
            builds = list()
            for raw_build in raw_builds:
                build = Build.from_dict(raw_build, [('finished_at', 'ended_at')])
                if build.created_by:
                    build.created_by = build.created_by.get('login')
                if build.duration:
                    build.duration *= 1000  # Convert to milliseconds
                else:
                    build.duration = 0
                build.workflow = raw_build.get('repository').get('name')
                build.branch = build.branch.get('name')
                build.used_tool = TRAVIS_CI
                build.test_results = self.get_test_results(raw_build)
                builds.append(build)
            return builds
        except TravisAccessorError:
            return []
