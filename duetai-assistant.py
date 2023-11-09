import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="duet-ai-test-400118", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison")
response = model.predict(
    """Classify the following.
Options:
- optimize for reliability
- optimize for cost
- workload recommendations
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
print(f"Response from Model: {response.text}")