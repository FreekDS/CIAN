import statistics
from typing import Any, Dict
from analyzer.utils.AnalysisCommand import AnalysisCommand


class BasicAnalysis(AnalysisCommand):

    def _get_builds_from_tool(self, tool):
        return list(filter(lambda build: build.used_tool == tool, self.builds))

    def _filter_state(self, state, tool=None):
        builds = self._get_builds_from_tool(tool) if tool else self.builds
        return list(filter(
            lambda build: build.state == state,
            builds
        ))

    def get_failing_builds(self, tool=None):
        return self._filter_state('failure', tool)

    def get_success_builds(self, tool=None):
        return self._filter_state('success', tool)

    def get_avg_duration(self, tool=None):
        builds = self._get_builds_from_tool(tool) if tool else self.builds
        if len(builds) == 0:
            return 0
        return statistics.mean(build.duration for build in builds if build.duration > 0)

    def get_builds_triggered_by(self, event, tool=None):
        builds = self._get_builds_from_tool(tool) if tool else self.builds
        return list(filter(
            lambda build: build.event_type == event,
            builds
        ))

    def execute(self) -> Dict[str, Any]:
        pass
