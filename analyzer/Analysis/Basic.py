import statistics
from typing import Any, Dict, List

from Builds import Build
from analyzer.utils.AnalysisCommand import AnalysisCommand
from analyzer.config import CI_TOOLS


class BasicAnalysis(AnalysisCommand):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, 'basic')

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
        analysis = dict()

        event_types = ['push', 'pull_request']

        def basic_info(d, t=None):
            d['failed_builds'] = len(self.get_failing_builds(t))
            d['successful_builds'] = len(self.get_success_builds(t))
            d['avg_duration'] = self.get_avg_duration(t)
            return d

        analysis = basic_info(analysis)

        # per tool analysis
        per_tool_analysis = dict()
        for tool in CI_TOOLS:
            tool_info = dict()
            tool_info = basic_info(tool_info, tool)
            per_tool_analysis[tool] = tool_info
        analysis['tools'] = per_tool_analysis

        # per event analysis
        per_event_analysis = dict()
        for event in event_types:
            per_event_analysis[event] = len(self.get_builds_triggered_by(event))
        analysis['builds_per_event'] = per_event_analysis

        return analysis

