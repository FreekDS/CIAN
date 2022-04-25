import pytest
import os
import shutil
from analyzer.Output.TextOutput import TextOutput
from analyzer.config import LATE_MERGING, SKIP_FAILING_TESTS, SLOW_BUILD, BROKEN_RELEASE


@pytest.fixture(scope='module')
def res_dir(data_dir):
    return os.path.join(data_dir, 'Output')


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


@pytest.fixture(scope='module')
def late_merging_data_hd(antipattern_data_hd):
    antipattern_data_hd[LATE_MERGING] = {
        'missed activity': {
            'branch1': 0,
            'branch2': 58748,
            'branch3': -1,
            'branch4': 1,
            'branch5': -20
        },
        'branch deviation': {
            'branch1': 0,
            'branch2': 20,
            'branch3': 30,
            'branch4': 5,
            'branch5': 1000
        },
        'unsynced activity': {
            'branch1': 0,
            'branch2': 20,
            'branch3': 30,
            'branch4': 5,
            'branch5': 1000
        },
        'classification': {
            'missed activity': {
                'medium_severity': ['branch5'],
                'high_severity': ['branch2']
            },
            'branch deviation': {
                'medium_severity': ['branch5'],
                'high_severity': ['branch2']
            },
            'unsynced activity': {
                'medium_severity': ['branch5'],
                'high_severity': ['branch2']
            }
        }
    }
    return antipattern_data_hd


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


def test_create_late_merging(late_merging_data_hd, res_dir):
    t_out = TextOutput(
        late_merging_data_hd,
        'some/repo-path',
        out_path='./some_output'
    )

    t_out.create_late_merging()

    assert os.path.exists(f'{t_out.out_path}/summary_late_merging.txt')

    with open(f'{t_out.out_path}/summary_late_merging.txt') as gen_f:
        with open(f'{res_dir}/summary_late_merging_ref.txt') as ref_f:
            assert gen_f.readlines() == ref_f.readlines()

    shutil.rmtree('./some_output')
    assert not os.path.exists(f'{t_out.out_path}/summary_late_merging.txt')
