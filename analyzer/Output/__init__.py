from .AntipatternGraphics import AntipatternGraphics


def create_images(anti_pattern_data, repo, out_path='./output'):
    graphics = AntipatternGraphics(anti_pattern_data, repo.name, repo.path, out_path=out_path)
    graphics.broken_release_graphics()
    graphics.slow_builds_graphic()
    graphics.skip_failing_tests_graphics()
