from typing import Dict, List, Any
from analyzer.ResultsCollector.PytestResults import PytestResult


result_collectors = [PytestResult]


def collect_test_results(log_file) -> List[Dict[str, Any]]:
    result = list()
    for Collector in result_collectors:
        collector = Collector(log_file)
        data = collector.execute()
        if data:
            result.append(data)
    return result
