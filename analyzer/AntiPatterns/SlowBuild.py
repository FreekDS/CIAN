import datetime

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List

import numpy as np

# TODO: classification is made per week, maybe it is more useful to have this per build


class SlowBuild(AntiPattern):
    def __init__(self, builds: List[Build], days_between=7):
        super().__init__(builds, name='slow_build')
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
            results[wf]["classification"] = self.classify(results[wf])

        return results

    @staticmethod
    def get_quartiles(durations):
        data = np.array(durations)
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        return {
            "q1": q1, "q3": q3, 'iqr': iqr
        }

    @staticmethod
    def classify(results_data):
        data_points = list(results_data.get("data").items())
        quartile_data = results_data.get('quartiles')

        high_severity = list(
            filter(
                lambda dp: dp[1] > quartile_data.get('q3') + 1.5 * quartile_data.get('iqr'),
                data_points
            )
        )
        medium_severity = list(
            filter(
                lambda dp: dp[1] > quartile_data.get('q3') and dp not in high_severity,
                data_points
            )
        )

        high_severity = {
            dp[0]: dp[1] for dp in high_severity
        }

        medium_severity = {
            dp[0]: dp[1] for dp in medium_severity
        }

        return {
            'high_severity': high_severity,
            'medium_severity': medium_severity
        }

    def detect(self):
        return self.average_duration_weekly()
