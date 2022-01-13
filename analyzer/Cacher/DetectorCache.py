import os
import json

# TODO create better caching mechanism
# TODO add tests for cacher


def hit(filepath='detection.cache'):
    return os.path.exists(filepath)


def create_cache(detect_result, filepath='detection.cache', override=False):
    if override or not hit(filepath):
        with open(filepath, 'w') as cache_file:
            cache_file.writelines(json.dumps(detect_result, indent=2))
            return True
    return False


def restore_cache(filepath='detection.cache'):
    if not hit(filepath):
        return list()
    with open(filepath, 'r') as cache_file:
        detect = json.load(cache_file)
        return detect
