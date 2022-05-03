from typing import Dict, List, Any
from analyzer.ResultsCollector.PytestResults import PytestResult
from analyzer.ResultsCollector.CTestResults import CTestResults
from analyzer.ResultsCollector.GTestResults import GTestResults
from analyzer.ResultsCollector.JUnitResults import JUnitResults
from analyzer.ResultsCollector.JestResults import JestResults
from analyzer.ResultsCollector.QUnitResults import QUnitResults


result_collectors = [
    PytestResult,
    CTestResults,
    GTestResults,
    JUnitResults,
    JestResults,
    QUnitResults
]


def collect_test_results(log_file) -> List[Dict[str, Any]]:
    result = list()
    for Collector in result_collectors:
        collector = Collector(log_file)
        data = collector.execute()
        if data:
            result.append(data)
    return result
