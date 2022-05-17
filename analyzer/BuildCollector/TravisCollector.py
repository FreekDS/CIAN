from typing import List
from collections import defaultdict

from analyzer.Repository.Repo import Repo
from analyzer.utils import format_date
from analyzer.Builds import Build
from analyzer.utils.Command import Command
# from analyzer.utils import timing
from analyzer.utils.TravisAccessor import TravisAccessor, TravisAccessorError
from analyzer.config import TRAVIS_CI
from analyzer.ResultsCollector import collect_test_results


class TravisCollector(Command):

    def __init__(self, repo: Repo, from_date=None, to_date=None):
        super().__init__()
        self.repo: Repo = repo
        self.travis_access = TravisAccessor()
        self.from_date = from_date
        self.to_date = to_date

    def get_test_results(self, raw_build):
        test_results = defaultdict(list)
        for job in raw_build.get('jobs', []):
            raw_job = self.travis_access.get_job(job.get('id'))
            if not raw_job:
                continue
            job_name = raw_job.get('name')
            log = self.travis_access.get_job_log(job.get('id'))
            if log:
                print("found log")
            tests = collect_test_results(log)
            if tests:
                test_results[job_name].append(tests)
        return dict(test_results)

    def attach_test_results(self, jobs_per_build, builds):
        job_ids = list()
        for jl in jobs_per_build:
            job_ids += [j.get('id', "-1") for j in jl]
        jobs = self.travis_access.collect_jobs(job_ids)
        logs = self.travis_access.collect_logs(job_ids)

        test_results = {j_id: collect_test_results(log) for j_id, log in logs.items()}
        for i, jobs_list in enumerate(jobs_per_build):
            results_for_build = defaultdict(list)
            for j_o in jobs_list:
                j_i = j_o.get('id', '')
                results_for_build[jobs.get(j_i, {}).get('name', "")].append(test_results.get(j_i, []))
            builds[i].test_results = dict(results_for_build)
        return builds

    # @timing
    def execute(self, *args, **kwargs) -> List[Build]:
        builds = list()
        jobs = list()
        try:
            raw_builds = self.travis_access.get_builds(self.repo)
            for raw_build in raw_builds:
                jobs.append(raw_build.get('jobs', []))
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
                # build.test_results = self.get_test_results(raw_build)
                builds.append(build)
            builds = self.attach_test_results(jobs, builds)
            if self.from_date:
                from_date = format_date(self.from_date)
                builds = list(
                    filter(
                        lambda b: b.start_date >= from_date,
                        builds
                    )
                )
            if self.to_date:
                to_date = format_date(self.to_date)
                builds = list(
                    filter(
                        lambda b: b.start_date <= to_date,
                        builds
                    )
                )
            return builds
        except TravisAccessorError as err:
            builds = self.attach_test_results(jobs, builds)
            if self.from_date:
                from_date = format_date(self.from_date)
                builds = list(
                    filter(
                        lambda b: format_date(b.start_date) >= from_date,
                        builds
                    )
                )
            if self.to_date:
                to_date = format_date(self.to_date)
                builds = list(
                    filter(
                        lambda b: format_date(b.start_date) <= to_date,
                        builds
                    )
                )
            return builds
