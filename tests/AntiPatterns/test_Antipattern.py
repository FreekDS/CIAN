from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build


class TestableAntipattern(AntiPattern):

    def detect(self) -> dict:
        pass


def test_sort_by_workflow():
    wf1 = 'wf1'
    wf2 = 'wf2'
    wf3 = 'wf3'
    builds = [
        Build(workflow=wf1),
        Build(workflow=wf1),
        Build(workflow=wf1),
        Build(workflow=wf2),
        Build(workflow=wf2),
    ]

    sorted_d = AntiPattern.sort_by_workflow(builds)
    assert len(sorted_d[wf1]) == 3
    assert len(sorted_d[wf2]) == 2
    assert wf3 not in sorted_d.keys()


def test_sort_chronologically():
    builds = [
        Build(started_at='2021-10-05T17:03:20Z', number=2, workflow='wf'),
        Build(started_at='2020-10-05T17:03:20Z', number=1, workflow='wf'),
        Build(started_at='2020-10-05T17:03:19Z', number=0, workflow='wf'),
    ]

    a = TestableAntipattern(builds)
    a.detect()

    sort = a.sort_chronologically()

    for i, b in enumerate(sort['wf']):
        assert b.number == i
