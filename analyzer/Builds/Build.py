from typing import List, Tuple
import datetime


class Build:

    @staticmethod
    def from_dict(d, translation_rules: List[Tuple[str, str]] = None):
        """
        List of tuples: each tuple has two strings: (key_old, key_new)
        """
        translation_rules = list() if not translation_rules else translation_rules
        for rule in translation_rules:
            if len(rule) < 2:
                continue
            if rule[0] != rule[1]:
                d[rule[1]] = d.pop(rule[0])
        return Build(**d)

    @staticmethod
    def format_date(date):
        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def start_date(self):
        return self.format_date(self.started_at)

    @property
    def end_date(self):
        return self.format_date(self.ended_at)

    def __init__(self, state=str(), id=int(), number=int(), started_at=str(), ended_at=str(), duration=int(),
                 created_by=str(), event_type=str(), branch=str(), used_tool=str(), test_results=None, workflow=str(),
                 **kwargs):
        self.state: str = state
        self.id: int = id
        self.number = int(number)
        self.started_at = started_at
        self.ended_at = ended_at
        self.duration = duration
        self.created_by = created_by
        self.event_type = event_type
        self.branch = branch
        self.used_tool = used_tool
        self.test_results = test_results if test_results else dict()
        self.workflow = workflow

    def __repr__(self):
        return str(self.dict())

    def dict(self):
        return self.__dict__
