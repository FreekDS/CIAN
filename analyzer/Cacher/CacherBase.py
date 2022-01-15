import json
import os


class CacherBase:

    DIR = "cache/"

    def __init__(self, repo_name, file_path):
        self.repo = repo_name
        self._fp_ext = file_path if file_path.endswith('.cache') else f'{file_path}.cache'
        self.fp = f'{self.DIR}{repo_name}-{self._fp_ext}'

    def hit(self):
        return os.path.exists(self.fp)

    def create(self, obj_to_cache, override=True):
        if not self.hit() or override:
            with open(self.fp, 'w') as cache_file:
                cache_file.writelines(json.dumps(obj_to_cache, indent=2))
                return True
        return False

    def restore(self, default=None):
        if not self.hit():
            return default
        with open(self.fp, 'r') as cache_file:
            return json.load(cache_file)

    def remove(self):
        if self.hit():
            os.remove(self.fp)
            return True
        return False
