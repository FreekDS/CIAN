from analyzer.Builds.Build import Build
from typing import List
import os
import json


def hit(filepath='builds.cache'):
    return os.path.exists(filepath)


def create_cache(builds: List[Build], filepath='builds.cache', override=False):
    if override or not hit(filepath):
        with open(filepath, 'w') as cache_file:
            builds = [b.dict() for b in builds]
            cache_file.writelines(json.dumps(builds, indent=2))
            return True
    return False


def restore_cache(filepath='builds.cache') -> List[Build]:
    if not hit(filepath):
        return list()
    with open(filepath, 'r') as cache_file:
        builds_json = json.load(cache_file)
        builds = [Build.from_dict(b) for b in builds_json]
        return builds
