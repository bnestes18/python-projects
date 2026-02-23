from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Step:
    name: str
    status: str          # "completed", "skipped", etc.
    conclusion: str      # "success", "failure", "skipped"
    started_at: datetime
    completed_at: datetime
    duration: timedelta  # computed at construction time

@dataclass 
class Job:
    id: int
    name: str
    status: str
    conclusion: str
    started_at: datetime
    completed_at: datetime
    duration: timedelta
    steps: list[Step]

@dataclass 
class WorkflowRun:
    id: int
    name: str
    run_number: int
    status: str
    conclusion: str
    created_at: datetime
    updated_at: datetime
    jobs: list[Job]    # populated separately after a second API call
        