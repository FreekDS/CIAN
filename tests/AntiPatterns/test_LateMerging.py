from analyzer.AntiPatterns.LateMerging import LATE_MERGING, LateMerging


def test_constructor():
    lm = LateMerging([], {})
    assert lm.builds == {}
    assert lm.name == LATE_MERGING
    assert lm.branch_info == {}


def test_missed_activity():
    t_lo = "1999-08-17T14:05:17Z"
    b_info = {
        'merged': True,
        'sync': "2000-08-17T10:05:17Z"
    }

    assert LateMerging.missed_activity(t_lo, b_info) == -366

    b_info['merged'] = False

    assert LateMerging.missed_activity(t_lo, b_info) == 0

    t_lo = "2000-08-17T10:05:17Z"
    b_info = {
        'merged': True,
        'sync': '1999-08-17T14:05:17Z'
    }

    assert LateMerging.missed_activity(t_lo, b_info) == 365

    t_lo = "1999-08-17T15:05:17Z"

    assert LateMerging.missed_activity(t_lo, b_info) == 0


def test_branch_deviation():
    t_lo = "2000-08-17T10:05:17Z"
    b_info = {
        'last_commit': "2000-08-13T10:05:17Z"
    }

    assert LateMerging.branch_deviation(t_lo, b_info) == 4

    b_info['last_commit'] = "2000-08-17T10:05:17Z"
    t_lo = "2000-08-13T10:05:17Z"

    assert LateMerging.branch_deviation(t_lo, b_info) == -4

    t_lo = "2000-08-17T10:05:17Z"

    assert LateMerging.branch_deviation(t_lo, b_info) == 0

    b_info['last_commit'] = 'unknown'

    assert LateMerging.branch_deviation(t_lo, b_info) == 0


def test_unsynced_activity():
    b_info = {
        'last_commit': "2000-08-17T10:05:17Z",
        "merged": True,
        "sync": "2000-07-17T10:05:17Z"
    }

    assert LateMerging.unsynced_activity(b_info) == 31

    b_info['merged'] = False

    assert LateMerging.unsynced_activity(b_info) == 0

    b_info["last_commit"] = "unknown"

    assert LateMerging.unsynced_activity(b_info) == 0


def test_classify():
    b_results = {
        'metric1': {
            'branch1': 5,
            'branch2': -5,
            'branch3': 0,
            'branch4': 1000,
            'branch5': -1000,
            'branch6': 17,
            'branch7': -17
        },
        'metric2': {
            'branch1': 5,
            'branch2': -5,
            'branch3': 0,
            'branch4': 1000,
            'branch5': -1000,
            'branch6': 17,
            'branch7': -17
        }
    }

    assert LateMerging.classify(b_results) == {
        'metric1': {
            'medium_severity': ['branch6', 'branch7'],
            'high_severity': ['branch4', 'branch5']
        },
        'metric2': {
            'medium_severity': ['branch6', 'branch7'],
            'high_severity': ['branch4', 'branch5']
        }
    }
