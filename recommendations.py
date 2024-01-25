# create a function to query a BigQuery table
from google.cloud import bigquery
from flask import Flask, jsonify

app = Flask(__name__)

def query_bigquery_table(project, location, cluster_name, controller_name, container_name ):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to query.
    # table_id = "your-project.your_dataset.your_table_name"

    query = """
    SELECT COUNT(DISTINCT(DATE(start_time))) metric_dates 
    FROM `gke-opt-demo.1034414536999_Metrics._AllMetrics`
    WHERE project_id = '{project}'
    AND location = '{location}'
    AND cluster_name = '{cluster_name}'
    AND controller_name = '{controller_name}'
    AND container_name = '{container_name}';
    """

    query_job = client.query(query)  # Make an API request.

    results = []
    for row in query_job:
        results.append(row)

    return results

def get_recommendation():
    return 0



@app.route('/', methods=['GET'])
def home():
    results = query_table()
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
