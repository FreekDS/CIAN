import os
from utils import format_date, format_date_str


class TextOutput:
    def __init__(self, data, repo_path, out_path='./output'):
        self.out_path = os.path.join(out_path, repo_path.replace('/', '-'))
        self.repo_path = repo_path.split('/')[0]
        os.makedirs(self.out_path, exist_ok=True)
        self.data = data

    def create_late_merging(self):
        pass

    def create_slow_build(self):
        pass

    def create_broken_release(self):
        pass

    def create_skip_failing_tests(self):
        pass
