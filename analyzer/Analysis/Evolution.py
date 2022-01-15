from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

from Builds import Build
from analyzer.utils.AnalysisCommand import AnalysisCommand


class EvolutionAnalysis(AnalysisCommand):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'evolution')
        self._sort_by_date()

    def _sort_by_date(self):
        self.builds.sort(
            key=lambda build: datetime.strptime(build.started_at, '%Y-%m-%dT%H:%M:%SZ')
        )

    def duration_over_time(self):
        data_points = list()
        for build in self.builds:
            data_points.append(
                (build.started_at, build.duration)
            )
        return data_points

    def _tests_over_time_with_status(self, status='test_count'):
        test_per_job = defaultdict(dict)
        for build in self.builds:
            test_results = build.test_results
            for job_name, test_counts_per_framework in test_results.items():
                if len(test_counts_per_framework[0]) == 0:
                    continue
                for entry in test_counts_per_framework:
                    framework = entry.get('framework', '')
                    if framework not in test_per_job[job_name]:
                        test_per_job[job_name][framework] = list()
                    test_per_job[job_name][framework].append(
                        (build.started_at, entry.get(status, 0))
                    )
        return test_per_job

    def tests_over_time(self):
        return self._tests_over_time_with_status()

    def successful_tests_over_time(self):
        return self._tests_over_time_with_status('successful_count')

    def failed_tests_over_time(self):
        return self._tests_over_time_with_status('failed_count')

    def skipped_tests_over_time(self):
        return self._tests_over_time_with_status('skipped_count')

    def execute(self) -> Dict[str, Any]:
        return {
            'duration': self.duration_over_time(),
            'tests': {
                'all': self.tests_over_time(),
                'success': self.successful_tests_over_time(),
                'failed': self.failed_tests_over_time(),
                'skipped': self.skipped_tests_over_time()
            }
        }
