import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.dates as md
import matplotlib.ticker as ticker


class SeabornPlotter:
    def __init__(self, repo_name, analysis_results):
        self.analysis_results = analysis_results
        self.repo = repo_name

    def duration_evolution(self):
        sns.set_style('ticks')
        sns.set_theme()
        data_points = self.analysis_results.get('evolution').get('duration')
        x = [datetime.strptime(d[0], '%Y-%m-%dT%H:%M:%SZ') for d in data_points]
        x = [x+1 for x in range(len(data_points))]
        y = [d[1] for d in data_points]
        ax = sns.barplot(
            x=x, y=y, palette='Blues_d'
        )
        plt.suptitle("Build duration over time")
        ax.set_title(self.repo)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

        ax.tick_params(axis='x', which='major', length=10)
        ax.tick_params(axis='x', which='minor', length=5)
        ax.set(xlabel="Build number", ylabel="duration (s)")
        plt.tight_layout()
        plt.savefig(f'{self.repo}-duration.png')
        plt.show()

    def test_evolution(self):
        # TODO: change data points to take build number rather than date
        data = self.analysis_results.get('evolution').get('tests').get('all')
        to_plot = list(data.items())[0][1]
        data_points = list(to_plot.values())[0]

        x = [i+1 for i in range(len(data_points))]
        y = [item[1] for item in data_points]

        ax = sns.lineplot(x=x, y=y)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax.tick_params(axis='x', which='major', length=10)
        ax.tick_params(axis='x', which='minor', length=5)
        ax.set(xlabel="Build number", ylabel="Test count")
        plt.suptitle("Test count over time")
        ax.set_title(self.repo)
        plt.tight_layout()
        plt.savefig(f'{self.repo}-tests.png')
        plt.show()
        print()
