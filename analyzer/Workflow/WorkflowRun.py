class WorkflowRun:
    def __init__(self, id, event, run_number, url, conclusion, jobs_url, artifacts_url):
        self.id = id
        self.run_number = run_number
        self.event = event
        self.url = url
        self.conclusion = conclusion
        self.jobs_url = jobs_url
        self.artifacts_url = artifacts_url

    def __repr__(self):
        return f"CIWorkflowRun(\n\t" \
               f"{self.id}\n\t" \
               f"{self.event}\n\t" \
               f"{self.conclusion}\n\t" \
               f"{self.jobs_url}"
