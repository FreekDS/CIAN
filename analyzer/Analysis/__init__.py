from .Basic import BasicAnalysis
from .Evolution import EvolutionAnalysis

# List of AnalysisCommand types
_analyzers = [BasicAnalysis, EvolutionAnalysis]


def analyse_builds(builds):
    analysis = dict()
    for analyzer in _analyzers:
        a = analyzer(builds)
        result = a.execute()
        analysis[a.name] = result
    return analysis


def available_analysis():
    return [a([]).name for a in _analyzers]
