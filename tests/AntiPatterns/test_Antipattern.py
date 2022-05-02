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


def test_sort_by_number():
    builds = [
        Build(number=2, workflow='wf'),
        Build(number=6, workflow='wf'),
        Build(number=4, workflow='wf'),
        Build(number=5, workflow='wf'),
        Build(number=500, workflow='wf'),
        Build(number=3, workflow='wf'),
        Build(number=7, workflow='wf'),
        Build(number=1, workflow='wf'),
        Build(number=0, workflow='wf'),
        Build(number=-50, workflow='wf'),
    ]

    a = TestableAntipattern(builds)
    a.detect()

    sort = a.sort_by_number()

    assert sort['wf'][0].number == -50
    assert sort['wf'][-1].number == 500

    for i, b in enumerate(sort['wf'][1:-1]):
        assert b.number == i
