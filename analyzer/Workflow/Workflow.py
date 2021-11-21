from typing import List, Tuple


class Workflow:
    def __init__(self, name, id, state, created_at, url, runs):
        self.name: str = name
        self.id = id
        self.state = state
        self.created_at = created_at
        self.url = url
        self.runs = runs

    def __repr__(self):
        return f"CIWorkflow(\n\t" \
               f"{self.name}\n\t" \
               f"{self.url}\n\t" \
               f"Runs: {len(self.runs)}\n" \
               f")"


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

    def __init__(self, state=str(), id=int(), number=int(), started_at=str(), ended_at=str(), duration=int(),
                 created_by=str(), event_type=str(), branch=str(), **kwargs):
        self.state: str = state
        self.id: int = id
        self.number = int(number)
        self.started_at = started_at
        self.ended_at = ended_at
        self.duration = duration
        self.created_by = created_by
        self.event_type = event_type
        self.branch = branch

    def __repr__(self):
        return str(self.__dict__)
