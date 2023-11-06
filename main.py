from google.cloud import bigquery
from google.cloud import monitoring_v3
import time

# Golden Signals metrics
def golden_signals_demand_based_down_scaling_cpu(project_id) -> None:
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

def golden_signals_demand_based_scaling_memory(project_id) -> None:
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
            "filter": 'metric.type = "kubernetes.io/node/memory/allocatable_utilization" AND memory_type != non-evictable',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

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
        WHERE run_date = CURRENT_DATE(); 
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row)

def top_overprovisioned() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE() AND priority > 0 
        ORDER BY priority DESC
        LIMIT 5
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row.controller_name)

def top_underprovisioned() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE() AND priority < 0
        ORDER BY priority ASC
        LIMIT 5
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row.controller_name)

def query_best_effort() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE() AND (cpu_requested_mcores = 0 or memory_requested_mib = 0)
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row.controller_name)

def query_workloads_at_risk() -> None:
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT *
        FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
        WHERE run_date = CURRENT_DATE() AND (cpu_request_utilization > 1 or memory_request_utilization > 1 )
        ORDER BY priority
        """
    )
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print(row.controller_name)
if __name__ == "__main__":
    golden_signals_demand_based_scaling_memory('gke-opt-demo')