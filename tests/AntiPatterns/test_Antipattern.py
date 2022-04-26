from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build


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
