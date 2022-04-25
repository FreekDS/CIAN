import pytest
import os
from analyzer.Output.TextOutput import TextOutput
from analyzer.config import LATE_MERGING, SKIP_FAILING_TESTS, SLOW_BUILD, BROKEN_RELEASE


@pytest.fixture(scope='module')
def antipattern_data_hd():
    """
    Happy day antipattern data
    :return: happy day antipattern data
    """
    return {
        LATE_MERGING: {},
        SKIP_FAILING_TESTS: {},
        SLOW_BUILD: {},
        BROKEN_RELEASE: {}
    }


def test_constructor(antipattern_data_hd):
    t_out = TextOutput(
        antipattern_data_hd,
        'some/repo-path',
        out_path='./some_output'
    )
    assert t_out.data == antipattern_data_hd
    path = os.path.join('./some_output', 'some-repo-path')
    assert t_out.out_path == path

    assert os.path.exists(path)

    # Test cleanup
    os.removedirs(path)
    assert not os.path.exists(path)
