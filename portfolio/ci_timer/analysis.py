from api import models
import helper
from operator import attrgetter
from datetime import timedelta
import logging

logger = logging.getLogger("Logger")
logging.basicConfig(level=logging.INFO)

# Parses key workflow data (steps, jobs, workflow run) into dataclasses and returns full workflow run. 
def parse_run(raw_run: dict, raw_jobs: list[dict]) -> models.WorkflowRun:
    # convert raw API dicts into dataclass objects
    jobs = helper.parse_jobs(raw_jobs)
    workflow = helper.parse_workflow(raw_run, jobs)
    return workflow

# Sorts jobs by duration in descending order and returns top n slowest jobs. Default number 'n' is 3 (jobs).
def find_bottlenecks(jobs: list[models.Job], top_n: int = 3) -> list[models.Job]:
  if top_n < 1:
    raise ValueError("top_n parameter must be greater than or equal to 1.")
  # TODO Consider adding more error handling here. Check if 'duration' key exists in provided jobs list

  # Filter out cancelled or in-progress runs
  valid_jobs = [j for j in jobs if j.duration is not None]
  
  jobs_sorted = sorted(valid_jobs, key=attrgetter('duration'), reverse=True)
  return jobs_sorted[:top_n]

# Returns a collections of stats from list of workflow jobs
def compute_summary_stats(jobs: list[models.Job]) -> dict:
  # Filter out cancelled or in-progress runs
  valid_jobs = [j for j in jobs if j.duration is not None]
      
  # TODO Consider adding error handling. Check for empty job param
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