import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="duet-ai-test-400118", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison")
response = model.predict(
    """Imagine you are a BigQuery expert with extensive knowledge in SQL querying. You are given a task to write an SQL query for a table named \'`gke-opt-demo.gke_metrics_dataset.workload_recommendations`\'. The table structure includes fields such as
run_date (DATE): The date on which the data was recorded. Useful for tracking metrics over time.
project_id (STRING): Identifier for the project within which the Kubernetes cluster is running. Helps in distinguishing between different projects or environments.
location (STRING): The geographical or cloud region where the Kubernetes cluster is hosted.
cluster_name (STRING): Name of the Kubernetes cluster. Useful for identifying which cluster the data pertains to.
controller_name (STRING): Name of the controller managing the Kubernetes workload. Controllers can be deployments, stateful sets, etc.
controller_type (STRING): Type of controller (e.g., Deployment, StatefulSet, DaemonSet) managing the workload.
namespace_name (STRING): Kubernetes namespace in which the workload is running. Namespaces are used to organize resources in a cluster.
container_name (STRING): Name of the specific container within a pod. A pod can have multiple containers.
cpu_mcore_usage (FLOAT): CPU usage in milli-core units. This shows how much CPU resource the workload is using.
memory_mib_usage_max (FLOAT): The maximum memory usage in Mebibytes (MiB). Indicates the peak memory usage.
cpu_requested_mcores (FLOAT): The amount of CPU resources in milli-cores requested by the workload. This is specified in the workload\'s configuration.
cpu_limit_mcores (FLOAT): The limit on CPU resources in milli-cores for the workload. This acts as an upper bound.
cpu_request_utilization (FLOAT): The utilization percentage of the requested CPU resources.
memory_requested_mib (FLOAT): The amount of memory in MiB requested by the workload.
memory_limit_mib (FLOAT): The upper limit on memory usage in MiB for the workload.
memory_request_utilization (FLOAT): Utilization percentage of the requested memory resources.
cpu_requested_recommendation (FLOAT): Suggested amount of CPU resources in milli-cores that should be requested based on usage patterns.
cpu_limit_recommendation (FLOAT): Suggested limit for CPU resources in milli-cores based on usage and performance considerations.
memory_requested_recommendation (FLOAT): Suggested amount of memory in MiB to be requested, based on historical usage data.
memory_limit_recommendation (FLOAT): Suggested memory limit in MiB, possibly to optimize performance and resource utilization.
priority (FLOAT): This could be an internal priority score or ranking used for provision status. If a workload\'s resources are over-provisioned, than the value is positive. The higher the value, the more over-provisioned the resources are and will cause extra cost. Negative numbers are under-provisioned. the smaller the number, the more under-provisioned the workload is and the higher risk for reliability.

Each of these fields plays a critical role in monitoring, scaling, and optimizing Kubernetes workloads, ensuring efficient resource allocation and utilization.

input: Are there any over-provisioned workloads that can be downsized without impacting performance?
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND 
 priority > 0 
ORDER BY priority DESC

input: Which workloads have the highest priority for optimization
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND priority < 0
ORDER BY priority ASC

input: Can any over-provisioned workloads be scaled down without impacting performance?
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND priority > 0
ORDER BY priority DESC

input: Which workloads are at reliability risk?
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND (cpu_requested_mcores = 0 OR memory_requested_mib = 0 OR cpu_request_utilization > 1 OR memory_request_utilization >1)
ORDER BY priority DESC

input: Is my cluster set up to scale nodes down during periods of low demand?
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND (cpu_requested_mcores = 0 OR memory_requested_mib = 0) OR
priority > 0
ORDER BY priority DESC

input: Which workloads might face challenges during high-traffic events like Black Friday, based on their current utilization and limits?
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND (cpu_request_utilization > 1 OR memory_request_utilization >1)
ORDER BY priority DESC

input: Which workloads that can be throttled to request to zero and become unresponsive
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND cpu_requested_mcores = 0
ORDER BY priority DESC

input: Which workloads that can be killed at any time causing a disruption
output: SELECT * FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1 AND memory_requested_mib = 0
ORDER BY priority DESC

input: How much can I save if I rightsized
output: SELECT 
SUM(cpu_requested_mcores - cpu_requested_recommendation) AS potential_mCPU_savings,
SUM(memory_requested_mib - memory_requested_recommendation) AS potential_MiB_avings,
FROM `gke-opt-demo.gke_metrics_dataset.workload_recommendations` 
WHERE run_date = CURRENT_DATE(\'EST\')-1

input: Where can I save on cost
output:
""",
    **parameters
)
print(f"Response from Model: {response.text}")