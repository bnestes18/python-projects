import os
import csv
from output import table
from output import chart
import api.models as models
from dataclasses import asdict
import datetime
import json
from enums import OutputType
import utils

# Routes workflow data and metrics to specific export types
def send(workflow_run: models.WorkflowRun, workflow_metrics: models.WorkflowMetrics, output: OutputType) -> None:
    if(output==OutputType.TABLE):
        table.render_table(workflow_run, workflow_metrics)
        print("exported to table")
    elif(output==OutputType.CHART):
        chart.render_chart(workflow_run, workflow_metrics)
        print("exported to chart")
    elif(output==OutputType.JSON):
        export_json(workflow_run, workflow_metrics)
        print("exported to json")
    elif(output==OutputType.CSV):
        export_csv(workflow_run)
        print("exported to csv")
    else:
        print("unsupported output type")

# Exports workflow data to json file
def export_json(run: models.WorkflowRun, metrics: models.WorkflowMetrics) -> None:   
    working_directory = os.getcwd()
    path = os.path.join(working_directory, f"workflow_{run.id}.{OutputType.JSON.value}")
    
    # Convert WorkflowRun to a dict
    run_dict = asdict(run)
    metrics_dict = asdict(metrics)
    serialized_run = utils.serialize_value(run_dict)
    serialized_metrics = utils.serialize_value(metrics_dict)
    
    # Set workflow key values
    keys = ["run", "metrics"]
    wf = dict.fromkeys(keys)
    wf["run"] = serialized_run
    wf["metrics"] = serialized_metrics
    
    # write json to file at current working directory
    wf_stats = json.dumps(wf)
    with open(path, "w") as f:
            f.write(wf_stats)

# Exports workflow data to csv file
def export_csv(run: models.WorkflowRun):
    working_directory = os.getcwd()
    path = os.path.join(working_directory, f"workflow_{run.id}.{OutputType.CSV.value}")
    
    flattened_jobs = []
    csv_headers = ["run_id", "job_name", "status", "conclusion", "started_at", "completed_at", "duration_seconds"]
    for job in run.jobs:
        flattened_jobs.append([
            run.id,
            job.name,
            job.status,
            job.conclusion,
            job.started_at.isoformat() if job.started_at else "--",
            job.completed_at.isoformat() if job.completed_at else "--",
            int(job.duration.total_seconds()) if job.duration else "--"
        ])
    
    # Write to csv file with given filename
    with open(path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_headers)
        csv_writer.writerows(flattened_jobs)