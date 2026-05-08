from api import models
import utils
from operator import attrgetter
from datetime import timedelta
import logging

logger = logging.getLogger("Logger")

# Parses key workflow data (steps, jobs, workflow run) into dataclasses and returns full workflow run. 
def parse_run(raw_run: dict, raw_jobs: list[dict]) -> models.WorkflowRun:
    # convert raw API dicts into dataclass objects
    jobs = utils.parse_jobs(raw_jobs)
    workflow = utils.parse_workflow(raw_run, jobs)
    return workflow

# Sorts jobs by duration in descending order and returns top n slowest jobs. Default number 'n' is 3 (jobs).
def find_bottlenecks(jobs: list[models.Job], top_n: int = 3) -> list[models.Job]:
  if top_n < 1:
    raise ValueError("top_n parameter must be greater than or equal to 1.")

  # Filter out cancelled or in-progress runs
  valid_jobs = [j for j in jobs if j.duration is not None]
  
  # Check number of jobs. There must be at least one.
  if not valid_jobs:
    raise ValueError("No completed jobs found in this workflow run. The run may have been cancelled or all jobs are still in progress")
  
  jobs_sorted = sorted(valid_jobs, key=attrgetter('duration'), reverse=True)
  return jobs_sorted[:top_n]

# Returns a collection of stats from list of workflow jobs
def compute_summary_stats(jobs: list[models.Job]) -> dict:
  # Filter out cancelled or in-progress runs
  valid_jobs = [j for j in jobs if j.duration is not None]
  
  # Check number of jobs. There must be at least one.
  if not valid_jobs:
    raise ValueError("No completed jobs found in this workflow run. The run may have been cancelled or all jobs are still in progress")

  total_job_duration = timedelta()

  # Sum all job durations
  for j in valid_jobs:
    total_job_duration += j.duration
  
  # Get full list of jobs
  jobs_list = sorted(valid_jobs, key=attrgetter('duration'), reverse=True)    
  
  # Set dictionary key values
  stats = {
    'total_job_duration': total_job_duration,
    'average_job_duration': total_job_duration / len(jobs_list),
    'longest_job':  jobs_list[0],
    'shortest_job': jobs_list[-1]
    
  }
  return stats