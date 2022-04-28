from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from analyzer.utils import format_date
from analyzer.config import LATE_MERGING
from typing import List

import numpy as np


class LateMerging(AntiPattern):

    def __init__(self, builds: List[Build], branch_info):
        super().__init__(builds, LATE_MERGING)
        self.branch_info = branch_info

    @staticmethod
    def missed_activity(t_lo, b_info):
        """t_ma = t_lo - t_sync"""
        t_lo = format_date(t_lo)
        if b_info.get('merged') is True:
            t_sync = format_date(b_info.get('sync'))
            t_ma = t_lo - t_sync
            return t_ma.days
        return 0

    @staticmethod
    def branch_deviation(t_lo, b_info):
        """t_bd = t_lo - t_lc"""
        t_lo = format_date(t_lo)
        t_lc = b_info.get('last_commit')
        if t_lc != 'unknown':
            t_lc = format_date(t_lc)
            t_bd = t_lo - t_lc
            return t_bd.days
        return 0

    @staticmethod
    def unsynced_activity(b_info):
        """t_ua = t_lc - t_sync"""
        t_lc = b_info.get('last_commit')
        if t_lc == 'unknown':
            return 0
        t_lc = format_date(t_lc)
        if not b_info.get('merged'):
            return 0
        t_sync = format_date(b_info.get('sync'))
        t_ua = t_lc - t_sync
        return t_ua.days

    @staticmethod
    def classify(b_results):

        results = dict()

        for metric, branches_info in b_results.items():

            results[metric] = dict()

            data = np.array(list(branches_info.values()))

            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1

            results[metric]['medium_severity'] = list(
                filter(
                    lambda key: q3 < abs(branches_info[key]) <= q3 + 1.5 * iqr,
                    branches_info
                )
            )

            results[metric]['high_severity'] = list(
                filter(
                    lambda key: abs(branches_info[key]) > q3 + 1.5 * iqr,
                    branches_info
                )
            )

        return results

    def detect(self) -> dict:
        result = dict()
        lo = self.branch_info.get('last_commit')

        result['missed activity'] = dict()
        result['branch deviation'] = dict()
        result['unsynced activity'] = dict()

        for b_name, info in list(self.branch_info.items())[1:]:
            result['missed activity'][b_name] = self.missed_activity(lo, info)
            result['branch deviation'][b_name] = self.branch_deviation(lo, info)
            result['unsynced activity'][b_name] = self.unsynced_activity(info)

        result['classification'] = self.classify(result)
        return result
