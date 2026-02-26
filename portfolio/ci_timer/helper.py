from api import models
from datetime import datetime

def parse_jobs(raw_jobs: list[dict]) -> list[models.Job]:
    jobs = []
    for j in raw_jobs:
        steps = []
        for s in j['steps']:
            # Convert date strings into datetime objects
            step_started_at_date = get_iso_datetime(s['started_at'])
            step_completed_at_date = get_iso_datetime(s['completed_at'])
            
            # Calculate step duration as long as there is a value for started_at and completed_at
            step_duration = (step_completed_at_date - step_started_at_date) if step_started_at_date and step_completed_at_date else None
            step = models.Step(
                name=s['name'],
                status=s['status'],
                conclusion=s['conclusion'],
                started_at=step_started_at_date,
                completed_at=step_completed_at_date,
                duration=step_duration
            )
            steps.append(step)
       
        # Convert date strings into datetime objects
        job_started_at_date = get_iso_datetime(j['started_at'])
        job_completed_at_date = get_iso_datetime(j['completed_at'])
        
        # Calculate job duration as long as there is a value for started_at and completed_at
        job_duration = (job_completed_at_date - job_started_at_date) if job_started_at_date and job_completed_at_date else None
        job = models.Job(
            id=int(j['id']),
            name=j['name'],
            status=j['status'],
            conclusion=j['conclusion'],
            started_at=job_started_at_date,
            completed_at=job_completed_at_date,
            duration=job_duration,
            steps=steps
        )
        jobs.append(job)
    return jobs

def parse_workflow(raw_run: dict, jobs: list[models.Job]) -> models.WorkflowRun:
    # Convert date strings into datetime objects
    created_at_date = get_iso_datetime(raw_run['created_at'])
    updated_at_date = get_iso_datetime(raw_run['updated_at'])
    wfr = models.WorkflowRun(
        id=int(raw_run['id']),
        name=raw_run['name'],
        run_number=int(raw_run['run_number']),
        status=raw_run['status'],
        conclusion=raw_run['conclusion'],
        created_at=created_at_date,
        updated_at=updated_at_date,
        jobs=jobs
    )
    return wfr

# Converts date string to Datetime Object (in ISO 8601 format)
def get_iso_datetime(date: str | None) -> datetime | None:
    # Cancelled or In-Progress runs will return 'None' for started_at and completed_at fields in both jobs and steps. 
    if date is None:
        return None
    return datetime.fromisoformat(date.replace("Z", "+00:00"))