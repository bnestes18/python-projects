from rich.console import Console
from ci_timer.api import models as models
import ci_timer.utils as utils

# Displays job duration in a horizontal bar chart
def render_chart(run: models.WorkflowRun, metrics: models.WorkflowMetrics) -> None:
    # Create a Rich Console object
    console = Console()
    
    # Get the longest duration among valid jobs. Value is used for scaling bar widths.
    longest_job_duration = metrics.stats["longest_job"].duration
    # Arbitrary number that defines maximum bar width
    max_width = 40
    
    bottlenecks_ids = {j.id for j in metrics.bottlenecks}
    console.print("\n[bold]Job Duration Chart[/bold]\n")
    
    for job in run.jobs:
        # Include 'Cancelled' jobs.
        if job.duration is None:
            formatted_duration = "--"
            console.print(f"[white]{job.name:<30}[/white] |{'░' * (max_width)}| {formatted_duration}")
        else:
            # Check for bottlenecks if any, and highlight them in red
            is_bottleneck = job.id in bottlenecks_ids
            job_style_str = f"[red]{job.name:<30}[/red]" if is_bottleneck else f"[white]{job.name:<30}[/white]"
            formatted_duration = utils.format_duration(job.duration)
            bar_width = int((job.duration / longest_job_duration) * max_width) 
            console.print(f"{job_style_str} |{'█' * bar_width}{'░' * (max_width - bar_width)}| {formatted_duration}")