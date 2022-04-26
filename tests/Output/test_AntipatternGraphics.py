import os
import shutil

from analyzer.Output.AntipatternGraphics import AntipatternGraphics


def test_constructor():
    expected_path = os.path.join('./t-out', 'some-path')
    g = AntipatternGraphics(
        {'data'}, 'repo', 'some-path', './t-out'
    )

    assert g.data == {'data'}
    assert g.out_path == expected_path
    assert os.path.exists(expected_path)

    shutil.rmtree('./t-out')
