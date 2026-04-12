from api import models

def send(workflow_run: models.WorkflowRun, workflow_metrics: models.WorkflowMetrics, output: str):
    if(output=="table"):
        print("exported to table")
    elif(output=="chart"):
        print("exported to chart")
    elif(output=="json"):
        print("exported to json")
    elif(output=="csv"):
        print("exported to csv")
    else:
        print("unsupported output type")