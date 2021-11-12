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
