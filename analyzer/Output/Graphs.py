import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.dates as md
import matplotlib.ticker as ticker


class SeabornPlotter:
    def __init__(self, analysis_results):
        self.analysis_results = analysis_results

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
        ax.set_title("Build duration over time")

        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

        ax.tick_params(axis='x', which='major', length=10)
        ax.tick_params(axis='x', which='minor', length=5)
        ax.set(xlabel="Build number", ylabel="duration (s)")
        plt.tight_layout()
        plt.show()
