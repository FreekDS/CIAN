import datetime

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List

import numpy as np

# TODO: add threshold parameters, when is a build slow?


class SlowBuild(AntiPattern):
    def __init__(self, builds: List[Build], days_between=7):
        super().__init__(builds)
        self.builds = self.sort_chronologically()
        self.days_between = days_between

    def average_duration_weekly(self):
        results = dict()

        def within_week(start_date: datetime.date, end_date: datetime.date):
            delta = end_date - start_date
            return int(delta.days) < self.days_between

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
            results[wf]['total avg'] = sum(results[wf]["data"].values()) / len(results[wf]["data"])
            results[wf]["quartiles"] = self.get_quartiles(list(results[wf]["data"].values()))

        return results

    def sort_chronologically(self):
        sorted_dict = dict()
        for wf, builds in self.builds.items():
            builds.sort(key=lambda build: build.start_date)
            sorted_dict[wf] = builds
        return sorted_dict

    @staticmethod
    def get_quartiles(durations):
        data = np.array(durations)
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        return {
            "q1": q1, "q3": q3, 'iqr': iqr
        }

    def detect(self):
        return self.average_duration_weekly()
