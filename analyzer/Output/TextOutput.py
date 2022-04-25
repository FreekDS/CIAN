import os


class TextOutput:
    def __init__(self, data, repo_path, out_path='./output'):
        self.out_path = os.path.join(out_path, repo_path.replace('/', '-'))
        os.makedirs(self.out_path, exist_ok=True)
        self.data = data

    def create_late_merging(self):
        late_merging = self.data.get('late_merging')
        if not late_merging:
            return

        text = str()

        missed_activity = late_merging.get('missed activity', {})
        branch_deviation = late_merging.get('branch deviation', {})
        unsynced_activity = late_merging.get('unsynced activity', {})

        classification = late_merging.get('classification')

        if missed_activity:
            text += 'Missed Activity\n=========================\n'
            for branch, value in missed_activity.items():
                if value != 0:
                    text += f"Branch {branch} has {value} days of missed activity!\n"
        if classification:
            ma_classification = classification.get('missed activity', {})
            text += "MEDIUM SEVERITY\n"
            for branch in ma_classification.get('medium_severity', []):
                text += f"Branch {branch}, {missed_activity.get('branch')} seconds\n"
                text += "HIGH SEVERITY\n"
            for branch in ma_classification.get('high_severity', []):
                text += f"Branch {branch}, {missed_activity.get('branch')} seconds\n"

        if branch_deviation:
            avg_deviation = sum(branch_deviation.values()) / float(len(list(branch_deviation.values())))

            text += "\nBranch Deviation\n=========================\n"
            text += f"Average deviation: {avg_deviation} days\n"
            for branch, value in branch_deviation.items():
                if value > avg_deviation:
                    text += f"Branch {branch} moved away from main with {value} days, {value - avg_deviation} more " \
                            f"than average\n"
        if classification:
            bd_classification = classification.get('branch deviation', {})
            text += "MEDIUM SEVERITY\n"
            for branch in bd_classification.get('medium_severity', []):
                text += f"Branch {branch}, {branch_deviation.get(branch)} days\n"
            text += "HIGH SEVERITY\n"
            for branch in bd_classification.get('high_severity', []):
                text += f"Branch {branch}, {branch_deviation.get(branch)} days\n"

        if unsynced_activity:
            avg_unsynced = sum(unsynced_activity.values()) / float(len(list(branch_deviation.values())))

            text += "\nUnsynced activity\n=========================\n"
            text += f"Average unsynced: {avg_unsynced} days\n"
            for branch, value in unsynced_activity.items():
                if value > avg_unsynced:
                    text += f"Branch {branch} is unsynced with {value} days, {value - avg_unsynced} more than" \
                            f"average\n"
        if classification:
            ua_classification = classification.get('unsynced activity', {})
            text += "MEDIUM SEVERITY\n"
            for branch in ua_classification.get('medium_severity', []):
                text += f"Branch {branch}, {unsynced_activity.get(branch)} days"
            text += "HIGH SEVERITY\n"
            for branch in ua_classification.get('high_severity'):
                text += f"Branch {branch}, {unsynced_activity.get(branch)} days"

        with open(f'{self.out_path}/summary_late_merging.txt', 'w') as out:
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
