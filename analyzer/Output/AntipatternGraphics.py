from matplotlib import pyplot as plt
import os


class AntipatternGraphics:

    def __init__(self, data, repo_name, out_path='./output'):
        self.out_path = os.path.join(out_path, repo_name)
        os.makedirs(self.out_path, exist_ok=True)
        self.data = data

    def slow_builds_graphic(self):
        slow_build = self.data.get('slow_build')

        for ci_workflow, wf_info in slow_build.items():
            data = wf_info.get('data')
            tool = wf_info.get('tool')
            avg = round(float(wf_info.get('total avg')) / 1000, 2)

            plt.figure(figsize=(10, 5))
            dates = [date.split('T')[0] for date in data.keys()]  # Strip time from start date
            values = [float(v) / 1000 for v in data.values()]  # Convert to seconds

            plt.bar(dates, values)
            plt.plot(dates, values, '-o', color='red')
            plt.xlabel("Start date of week")
            plt.ylabel("Average build time of that week (s)")
            plt.suptitle(f"Slow build for '{ci_workflow}'")
            plt.title(f"Tool: '{tool}' avg duration: {avg}s")
            plt.xticks(rotation='vertical')

            plt.savefig(f"{self.out_path}/slow-build_{tool}.png", bbox_inches='tight')
