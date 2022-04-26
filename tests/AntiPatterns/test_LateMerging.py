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
