import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import os

from analyzer.utils import format_date, format_date_str
from collections import defaultdict


class AntipatternGraphics:

    def __init__(self, data, repo_name, repo_path, out_path='./output'):
        self.out_path = os.path.join(out_path, repo_path.replace('/', '-'))
        os.makedirs(self.out_path, exist_ok=True)
        self.data = data
        self.repo_name = repo_name

    @staticmethod
    def linreg(x, y):
        """
            return a,b in solution to y = ax + b such that root-mean-square distance between trend line and original points
            is minimized
            https://stackoverflow.com/questions/10048571/python-finding-a-trend-in-a-set-of-numbers
        """
        N = len(x)
        Sx = Sy = Sxx = Syy = Sxy = 0.0
        for x, y in zip(x, y):
            Sx = Sx + x
            Sy = Sy + y
            Sxx = Sxx + x * x
            Syy = Syy + y * y
            Sxy = Sxy + x * y
        det = Sxx * N - Sx * Sx
        return (Sxy * N - Sy * Sx) / det, (Sxx * Sy - Sx * Sxy) / det

    def slow_builds_graphic(self):
        slow_build = self.data.get('slow_build')
        if not slow_build:
            return

        tool_counter = defaultdict(int)

        for ci_workflow, wf_info in slow_build.items():
            data = wf_info.get('data')
            tool = wf_info.get('tool')
            avg = round(float(wf_info.get('total avg')) / 1000, 2)

            if data.get(None) is not None:
                del data[None]
            plt.figure(figsize=(10, 5))
            dates = [date.split('T')[0] for date in data.keys()]  # Strip time from start date
            values = [float(v) / 1000 for v in data.values()]  # Convert to seconds

            plt.bar(dates, values)
            plt.gca().set_ylim(bottom=0.)

            if len(values) > 1:
                x = np.linspace(0, len(dates), 100)
                a, b = self.linreg(
                    list(range(0, len(values))),
                    values
                )
                y = a * x + b
                c = 'green' if a < 0 else 'red'
                plt.plot(x, y, color=c)

            plt.xlabel("Start date of week")
            plt.ylabel("Average build time of that week (s)")
            plt.suptitle(f"Slow build for {self.repo_name} ({ci_workflow})")
            plt.title(f"Tool: '{tool}' avg duration: {avg}s")
            plt.xticks(rotation='vertical')

            plt.savefig(f"{self.out_path}/slow-build_{tool}_{tool_counter[tool]}.png", bbox_inches='tight')
            tool_counter[tool] += 1
            plt.close()

    def broken_release_graphics(self, time_between=7):
        broken_release = self.data.get('broken_release')
        if not broken_release:
            return

        tool_counter = defaultdict(int)

        for ci_workflow, wf_info in broken_release.items():

            data = wf_info.get('data')
            if not data:
                continue

            tool = wf_info.get('tool', '')

            ctr = 0
            first_date = None
            check_until = None

            weekly = dict()

            for broken_build in data:
                start_date = format_date(broken_build.get('started_at'))
                if not start_date:
                    continue
                if not first_date:
                    first_date = start_date
                    check_until = first_date + datetime.timedelta(days=time_between)

                if start_date <= check_until:
                    ctr += 1
                else:
                    weekly[format_date_str(first_date)] = ctr
                    missed_weeks = (start_date - check_until).days // 7
                    for _ in range(missed_weeks):
                        first_date = first_date + datetime.timedelta(days=time_between)
                        weekly[format_date_str(first_date)] = 0
                    ctr = 0
                    first_date = None

            if first_date:
                weekly[format_date_str(first_date)] = ctr

            ax = plt.figure(figsize=(10, 5)).gca()
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            dates = [date.split('T')[0] for date in weekly.keys()]
            values = list(weekly.values())
            if not dates:
                dates = ['none']
                values = [0]

            plt.bar(dates, values)

            if len(values) > 1:
                x = np.linspace(0, len(dates), 100)
                a, b = self.linreg(
                    list(range(0, len(values))),
                    values
                )
                y = a * x + b
                c = 'green' if a < 0 else 'red'
                plt.plot(x, y, color=c)

            # plt.plot(dates, values, '-o', color='red')
            plt.xlabel("Start date of week")

            # import matplotlib.dates as mdates

            # lc = mdates.WeekdayLocator(interval=1)
            # plt.gca().xaxis.set_major_locator(lc)

            plt.ylabel("Amount of failing release builds")
            plt.xticks(rotation='vertical')
            ax.set_ylim(bottom=0.)
            plt.suptitle(f"Broken Release for {self.repo_name} ({ci_workflow})")
            plt.title(f"Tool: '{tool}'")

            plt.savefig(f"{self.out_path}/broken-release_{tool}_{tool_counter[tool]}.png", bbox_inches='tight')
            tool_counter[tool] += 1
            plt.close()

    def skip_failing_tests_graphics(self):
        # skip_failing_tests = self.data.get('skip_failing_tests')
        # TODO implement if data is gathered
        return
