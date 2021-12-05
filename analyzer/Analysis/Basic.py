from typing import Any, Dict
from analyzer.utils.AnalysisCommand import AnalysisCommand


class BasicAnalysis(AnalysisCommand):

    def get_failing_builds(self, tool=None):
        pass

    def get_success_builds(self, tool=None):
        pass

    def get_avg_duration(self, tool=None):
        pass

    def get_builds_triggered_by(self, event):
        pass

    def execute(self) -> Dict[str, Any]:
        pass
