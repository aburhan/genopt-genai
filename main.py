from google.cloud import bigquery
from google.cloud import monitoring_v3
import time
from kubernetes import client, config
import json
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.language_models import CodeChatModel
from prettytable import PrettyTable
import sys

# Golden Signals - Cluster binpacking
def golden_signals_cluster_binpacking_cpu(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/node/cpu/allocatable_utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

def golden_signals_cluster_binpacking_memory(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/node/memory/allocatable_utilization" AND metric.label."memory_type" != "non-evictable"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

# Golden Signals - Workload rightsizing
def golden_signals_workload_rightizing_cpu(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/container/cpu/request_utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

def golden_signals_workload_rightizing_memory(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/container/memory/request_utilization" AND metric.label."memory_type" != "non-evictable"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

# Golden Signals - Demand based downscaling
def golden_signals_demand_based_downscaling(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/container/cpu/request_utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

# Golden Signals - Discount group
def golden_signals_discount_group(project_id) -> None:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 259200), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 259200}, 
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
            "group_by_fields": [],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "kubernetes.io/container/memory/request_utilization" AND metric.label."memory_type" != "non-evictable"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

# Workload recommendations
def optimization_summary() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT 
        (SUM(cpu_requested_mcores) - SUM(cpu_requested_recommendation)) AS cpu_provision_status,
        (SUM(memory_requested_mib) - SUM(memory_requested_recommendation))  AS memory_provision_status,
        COUNT(DISTINCT project_id) AS distinct_project_ids,
        COUNT(DISTINCT cluster_name) AS distinct_clusters,
        COUNT(*) AS workloads_analyzed,
        COUNT(CASE WHEN cpu_requested_mcores = 0 THEN 1 END) AS cpu_not_set,
        COUNT(CASE WHEN memory_requested_mib = 0 THEN 1 END) AS memory_not_set,
        COUNT(CASE WHEN cpu_request_utilization > 1 THEN 1 END) AS cpu_request_utilization_exceeded,
        COUNT(CASE WHEN memory_request_utilization > 1 THEN 1 END) AS memory_request_utilization_exceeded,
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST'); 
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)

def top_overprovisioned():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST') AND priority > 0 
        ORDER BY priority DESC
        LIMIT 5
        """
    )
    results = query_job.result()  # Waits for job to complete.


    over_provisioned_by = 0
    count = 0
    
    # Create a PrettyTable
    table = PrettyTable()
    table.field_names = ["Project", "Cluster", "Workload", "CPU_usage","CPU_request_recommendation", "CPU_limit_recommendation", "Max_memory_usage", "Memory_request_recommendation","Memory_limit_recommendation"]
    len(table.field_names)
    for row in results:
        count += 1
        workload = (( row.project_id, row.cluster_name, row.controller_name, row.cpu_mcore_usage, row.cpu_requested_recommendation, row.cpu_limit_recommendation, row.memory_mib_usage_max, row.memory_requested_recommendation, row.memory_limit_recommendation))
        table.add_row(workload)
        over_provisioned_by += (row.cpu_requested_mcores - row.cpu_requested_recommendation)

    return("The following {} workloads are over provisioned by {} mCores. \nOver-provisioned workloads :\n{} ".format(count, over_provisioned_by,table))
    


def top_underprovisioned():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST') AND priority < 0
        ORDER BY priority ASC
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)
    

def query_best_effort():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST') AND (cpu_requested_mcores = 0 or memory_requested_mib = 0)
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)
    

def query_workloads_at_risk() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST') AND (cpu_request_utilization > 1 or memory_request_utilization > 1 )
        ORDER BY priority
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)

def current_recommendations() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` WHERE run_date=CURRENT_DATE()-1
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)

# Kubectl 
def kubectl():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default")
    json_string = json.dumps
    for i in ret.items:
        print(type(ret))

        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def code_llm(controller_name):
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT controller_name, namespace_name, controller_type, cpu_requested_recommendation, cpu_limit_recommendation, memory_requested_recommendation, memory_limit_recommendation
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE('EST') AND (cpu_request_utilization > 1 or memory_request_utilization > 1 )
        ORDER BY priority
        """
    )
    results = query_job.result()  # Waits for job to complete.

    controller_name = ""
    namespace_name = ""
    controller_type = ""
    cpu_requested_recommendation = ""
    cpu_limit_recommendation = ""
    memory_requested_recommendation = ""
    memory_limit_recommendation = ""
    for row in results:
        controller_name = row.controller_name
        namespace_name = row.namespace_name
        controller_type = row.controller_type
        cpu_requested_recommendation = row.cpu_requested_recommendation
        cpu_limit_recommendation = row.cpu_limit_recommendation
        memory_requested_recommendation = row.memory_requested_recommendation
        memory_limit_recommendation = row.memory_limit_recommendation 

    vertexai.init(project="gke-opt-demo", location="us-central1")
    chat_model = CodeChatModel.from_pretrained("codechat-bison")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2
    }
    chat = chat_model.start_chat()
    #response = chat.send_message("""Create a kubernetes {controller_type} for a service called {controller_name} in namespace {namespace_name} with resource request for cpu = {cpu_requested_recommendation} cpu limit = {cpu_limit_recommendation} and memory request = {memory_requested_recommendation} memory limit {memory_limit_recommendation}""", **parameters)
    response = chat.send_message("""Create a kubernetes deployment for a service called adservice in namespace default with resource request for cpu = 8 cpu limit = 12 and memory request = 116 memory limit 116""", **parameters)

    print(f"Response from Model: {response.text}")

def text_llm(input): 
    vertexai.init(project="gke-opt-demo", location="us-central1")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 869,
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 2
    }
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        """Classify the following.
    Options:
    - optimize for reliability
    - optimize for cost
    - workload recommendations
    - contains service
    If the text doesn\'t fit any option, classify it as the following:
    - unknown

    Text: Are there any recommendations that I should consider implementing?
    The answer is: workload recommendations
    Text: Are there any over-provisioned workloads that can be downsized without impacting performance?
    The answer is: optimize for cost
    Text: Which workloads have the highest priority for optimization
    The answer is: optimize for reliability
    Text: Analyze how well my workload are optimized for cost
    The answer is: optimize for cost
    Text: How do the actual resource usages of my pods compare to their configured requests and limits?
    The answer is: workload recommendations
    Text: Can any over-provisioned resources be scaled down without impacting performance?
    The answer is: optimize for cost
    Text: Are my critical services using appropriate resource requests and limits to ensure Quality of Service (QoS)?
    The answer is: optimize for reliability
    Text: Is my cluster set up to scale nodes down during periods of low demand?
    The answer is: workload recommendations
    Text: Which workloads might face challenges during high-traffic events like Black Friday, based on their current utilization and limits?
    The answer is: optimize for reliability


    Text: How can I save money on my GKE workloads?
    The answer is:""",
        **parameters
    )
    return(response.text)

if __name__ == "__main__":
    
    # Categorize question
    print("Enter your optimzation question: ")
    question = sys.stdin.readline()
    if "service" in question:
        print(code_llm(question))
    else:
        response = text_llm(question)
        
        # Call related method
        if "optimize for reliability" in response :
            print(top_underprovisioned())
        elif "optimize for cost" in response :
            print(top_overprovisioned())
        elif "workload recommendations" in response :
            print(current_recommendations())   
        else:
            print("Answer not found") #update this to present best practice?
            print(0)
