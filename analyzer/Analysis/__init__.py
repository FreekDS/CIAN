from .Basic import BasicAnalysis

# List of AnalysisCommand types
_analyzers = [BasicAnalysis]


def analyse_builds(builds):
    analysis = dict()
    for analyzer in _analyzers:
        a = analyzer(builds)
        result = a.execute()
        analysis[a.name] = result
    return analysis
