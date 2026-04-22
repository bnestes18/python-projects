from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
import api.models as models
import utils

# Displays workflow run statistics in a Tabular format
def render_table(run: models.WorkflowRun, metrics: models.WorkflowMetrics):
    console = Console()
    # create Rich's Table
    table = Table(title="Workflow Stats")
    table.add_column("Job Name", justify="left")
    table.add_column("Conclusion", justify="center")
    table.add_column("Duration", justify="center")
    table.add_column("% of Total Duration", justify="center")
    table.add_column("Flag", justify="center", )

    bottlenecks_ids = {j.id for j in metrics.bottlenecks}
    
    for job in run.jobs:
        # Set warning flag and row styling if any job is detected in list of bottlenecks
        is_bottleneck = job.id in bottlenecks_ids
        warn = ":warning:" if is_bottleneck else ""
        style = "red" if is_bottleneck else ""
    
        # Set style for Job Conclusion for better readability
        conclusion_str = set_conclusion_style(job)
        
        # "Skipped" or "Canceled" jobs will not have a job.duration value. Need to render a friendly non-value to user.
        if job.duration is None:
            formatted_duration = "--"
            percent_of_total_duration = "--"
        else:    
            # else, proceed with rendering metrics for "Successful" jobs  
            formatted_duration = utils.format_duration(job.duration)
            percent_of_total_duration = '{:.0f}%'.format(job.duration / metrics.stats["total_job_duration"] * 100)
            
        # Populate row with job stats
        table.add_row(job.name, conclusion_str, formatted_duration, percent_of_total_duration, warn, style=style)
    
    summary = create_summary_template(metrics)
    
    # Render table and summary
    console.print(Align.center(table))
    console.print(Align.center(Columns(summary)))

# Sets a specific color style based on job conclusion value
def set_conclusion_style(job: models.Job) -> str:
    conclusion_colors = {
            "success": "green",
            "failure": "red",
            "skipped": "yellow",
            "cancelled": "dim"
        }
    color = conclusion_colors.get(job.conclusion, "white")
    return f"[{color}]{job.conclusion}[/{color}]"

# Creates a summary of computed stats from given workflow run 
def create_summary_template(metrics: models.WorkflowMetrics) -> list[Panel]:
    total_job_duration = utils.format_duration(metrics.stats['total_job_duration'])
    avg_job_duration = utils.format_duration(metrics.stats['average_job_duration'])
    
    return [
        Panel(total_job_duration, title="Total Job Duration"),
        Panel(avg_job_duration, title="Avg Job Duration"),
        Panel(str(metrics.stats['longest_job'].name), title="Longest Job"),
        Panel(str(metrics.stats['shortest_job'].name), title="Shortest Job"),
    ]