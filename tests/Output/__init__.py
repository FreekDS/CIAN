import pytest
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


@pytest.fixture(scope='module')
def late_merging_data_some_missing(late_merging_data_hd):
    del late_merging_data_hd[LATE_MERGING]['classification']
    del late_merging_data_hd[LATE_MERGING]['branch deviation']
    return late_merging_data_hd
