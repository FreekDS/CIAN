from .AntipatternGraphics import AntipatternGraphics
from .TextOutput import TextOutput
import os
import json


def create_images(anti_pattern_data, repo, out_path='./output'):
    graphics = AntipatternGraphics(anti_pattern_data, repo.name, repo.path, out_path=out_path)
    graphics.broken_release_graphics()
    graphics.slow_builds_graphic()
    graphics.skip_failing_tests_graphics()


def create_json(anti_pattern_data, repo, out_path='./output'):
    out_path = os.path.join(out_path, repo.path.replace('/', '-'))
    os.makedirs(out_path, exist_ok=True)

    with open(f'{out_path}/anti-patterns.json', 'w') as file:
        file.writelines(json.dumps(anti_pattern_data, indent=2))


def create_text_files(anti_pattern_data, repo, out_path='./output'):
    texts = TextOutput(anti_pattern_data, repo.path, out_path)
    texts.create_slow_build()
    texts.create_late_merging()
    texts.create_broken_release()
    texts.create_skip_failing_tests()
