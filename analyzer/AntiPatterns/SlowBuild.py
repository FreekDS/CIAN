import datetime

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List

# TODO: add threshold parameters, when is a build slow?


class SlowBuild(AntiPattern):
    def __init__(self, builds: List[Build]):
        super().__init__(builds)
        self.builds = self.sort_chronologically()

    def average_duration_weekly(self):
        results = dict()

        def within_week(start_date: datetime.date, end_date: datetime.date):
            delta = end_date - start_date
            return int(delta.days) < 7

        builds: List[Build]
        for wf, builds in self.builds.items():
            results[wf] = dict()
            results[wf]['data'] = dict()
            current_start_date = builds[0].start_date
            current_date_str = builds[0].started_at
            time_sum = builds[0].duration
            date_count = 1
            for build in builds[1:]:
                if within_week(current_start_date, build.start_date):
                    time_sum += build.duration
                    date_count += 1
                else:
                    results[wf]['data'][current_date_str] = time_sum / date_count
                    time_sum = build.duration
                    current_date_str = build.started_at
                    current_start_date = build.start_date
                    date_count = 1
            results[wf]['data'][current_date_str] = time_sum / date_count

            # Builds from different tools have different names:
            results[wf]['tool'] = builds[-1].used_tool

        return results

    def sort_chronologically(self):
        sorted_dict = dict()
        for wf, builds in self.builds.items():
            builds.sort(key=lambda build: build.start_date)
            sorted_dict[wf] = builds
        return sorted_dict

    def detect(self):
        return self.average_duration_weekly()
