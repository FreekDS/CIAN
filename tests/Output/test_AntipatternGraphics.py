import os
import shutil

from analyzer.Output.AntipatternGraphics import AntipatternGraphics
from tests.Output import slow_build_hd, antipattern_data_hd


def test_constructor():
    expected_path = os.path.join('./t-out', 'some-path')
    g = AntipatternGraphics(
        {'data'}, 'repo', 'some-path', './t-out'
    )

    assert g.data == {'data'}
    assert g.out_path == expected_path
    assert os.path.exists(expected_path)

    shutil.rmtree('./t-out')


def test_create_slow_build(slow_build_hd):
    g = AntipatternGraphics(slow_build_hd, 'repo', 'some-path', './t-out')
    g.slow_builds_graphic()
    file_count = len(os.listdir(g.out_path))
    assert file_count == 2

    shutil.rmtree('./t-out')
