import os
from utils import format_date, format_date_str


class TextOutput:
    def __init__(self, data, repo_path, out_path='./output'):
        self.out_path = os.path.join(out_path, repo_path.replace('/', '-'))
        self.repo_path = repo_path.split('/')[0]
        os.makedirs(self.out_path, exist_ok=True)
        self.data = data

    def create_late_merging(self):
        late_merging = self.data.get('late_merging')
        if not late_merging:
            return

        text = str()

        # TODO classification printing

        missed_activity = self.data.get('missed activity', {})
        branch_deviation = self.data.get('branch_deviation', {})
        unsynced_activity = self.data.get('unsynced_activity', {})

        text += 'Missed Activity\n=========================\n'
        for branch, value in missed_activity.items():
            if value != 0:
                text += f"Branch {branch} has {value} days of missed activity!\n"

        avg_deviation = sum(branch_deviation.values()) / float(len(list(branch_deviation.values())))

        text += "\nBranch Deviation\n=========================\n"
        text += f"Average deviation: {avg_deviation} days"
        for branch, value in branch_deviation.items():
            if value > avg_deviation:
                text += f"Branch {branch} moved away from main with {value} days, {value - avg_deviation} more " \
                        f"than average"

        avg_unsynced = sum(unsynced_activity.values() / float(len(list(branch_deviation.values()))))

        text += "\nUnsynced activity\n=========================\n"
        text += f"Average unsynced: {avg_deviation} days"
        for branch, value in unsynced_activity.items():
            if value > avg_unsynced:
                text += f"Branch {branch} is unsynced with {value} days, {value - avg_unsynced} more than" \
                        f"average"

        with open(f'{self.out_path}/summary_late_merging.txt') as out:
            out.write(text)

    def create_slow_build(self):
        slow_build = self.data.get('slow_build')
        if not slow_build:
            return
        pass

    def create_broken_release(self):
        broken_release = self.data.get('broken_release')
        if not broken_release:
            return
        pass

    def create_skip_failing_tests(self):
        skip_failing_tests = self.data.get('skip_failing_tests')
        if not skip_failing_tests:
            return
        pass
