from typer import Typer
import re
import logging
from config import DEFAULT_LIMIT, DEFAULT_OUTPUT, DEFAULT_TOP_N, resolve_token
from api import client
from api import models
import analysis
from output import export

logger = logging.getLogger("ci_timer")
logging.basicConfig(level=logging.INFO)

app = Typer()

@app.command()
def analyze(
    repo: str,                             # i.e. owner/repo
    run_id: int | None = None,             # if omitted, grab the most recent run
    top: int = DEFAULT_TOP_N,              # how many bottlenecks to highlight
    output: str = DEFAULT_OUTPUT,          # "table", "chart", "json", "csv"
    limit: int = DEFAULT_LIMIT,            # how many recent runs to fetch if no run_id provided
    token: str | None = None
):
    # Load token from config (env var or config file)
    cli_token = resolve_token(token)
        
    # Split repo into owner + repo_name
    if not repo:
        raise ValueError("Repo name not found. Please provide a name in 'owner/repo' format")
    
    repo_pattern = r"^([\w.-]+)\/([\w.-]+)$"
    repo_match = re.search(repo_pattern, repo)
    if not repo_match:
        logger.critical("Invalid repo name")
        raise ValueError(f"[{repo}] is invalid. Please ensure repository exists and has format 'owner/repo_name'.")
    # else, repository name is valid. Parse owner and repository name.
    owner = repo_match[1]
    repo_name = repo_match[2]
        
    # Instantiate GitHubClient with token
    with client.GitHubClient(cli_token) as c:
        # Fetch workflow run's jobs directly if run_id provided
        if run_id:
            raw_jobs = c.get_jobs_for_run(owner, repo_name, run_id)
            run = c.get_workflow_run_by_id(owner, repo_name, run_id)
        # else, fetch recent runs and pick the first (or last N if limit > 1)
        else:
            run = c.get_workflow_runs(owner, repo_name, limit)[0]
            raw_jobs = c.get_jobs_for_run(owner, repo_name, run["id"])
        
        # Build the WorkflowRun model
        wfr = analysis.parse_run(run, raw_jobs)
        
        # Generate metrics
        metrics = models.WorkflowMetrics(
            bottlenecks=analysis.find_bottlenecks(wfr.jobs, top),
            stats=analysis.compute_summary_stats(wfr.jobs)
        )
        
        # Route to the right output function based on --output flag
        export.send(wfr, metrics, output)