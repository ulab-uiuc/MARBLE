import os
import subprocess
import time
from typing import Any, Dict, List
import re

import numpy as np
import requests
from db_utils.anomaly_detection import detect_anomalies, describe_data_features

from marble.environments.base_env import BaseEnvironment

from db_utils.metrics import allowed_metrics_full_names, full_metrics_full_names
from db_utils.diagnostic_kb import DiagnosticKB

def get_prometheus_metric_data(metric_name: str) -> List[List[Any]]:
    """
    Query Prometheus for the given metric data from the last hour, sampling every 60 seconds.

    Args:
        metric_name (str): The name of the metric to retrieve (e.g., 'node:cpu:usage_avg1m').

    Returns:
        List[List[Any]]: A list of timestamp-value pairs for the metric over the past 10 minutes.
    """
    # Get the current time in Unix timestamp
    end_time = time.time()

    # Calculate the start time (10 minutes ago)
    start_time = end_time - 600  # 600 seconds = 10 minutes

    # Prometheus query range URL
    prom_url = 'http://localhost:9090/api/v1/query_range'

    # Parameters for the query
    params = {
        'query': metric_name,
        'start': start_time,
        'end': end_time,
        'step': 1  # sample every second
    }

    # Make the HTTP request to Prometheus
    response = requests.get(prom_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            # Extract the values (timestamp-value pairs) from the response
            try:
                return data['data']['result'][0]['values']
            except:
                return []
        else:
            raise ValueError(f"Prometheus returned an error: {data.get('error', 'Unknown error')}")
    else:
        raise ValueError(f"Failed to query Prometheus. Status code: {response.status_code}")

class DBEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str = "DBEnv"):
        """
        Initialize the DBEnvironment.

        Args:
            name (str): The name of the environment.
        """
        super().__init__(name, config)

        self.kb = DiagnosticKB()

        os.chdir('./db_env_docker')
        print("Starting Docker containers...")

        # Run docker-compose up in detached mode
        subprocess.run(["docker", "compose", "down", "-v"], shell=False, check=True)

        # Then, run "docker-compose up
        subprocess.run(["docker", "compose", "up", "-d", "--remove-orphans"], check=True)

        # anomalies
        env_configs = config.get('environment', [])

        if env_configs:
            anomalies = config.get('anomalies', [])
            for anomaly in anomalies:
                anomaly_type = anomaly['anomaly']
                threads = anomaly['threads']
                ncolumn = anomaly['ncolumn']
                colsize = anomaly['colsize']
                subprocess.run(["python3", "anomaly_trigger/main.py", "--anomaly", anomaly_type, "--threads", f"{threads}", "--ncolumn", f"{ncolumn}", "--colsize", f"{colsize}"], check=True)

        # We will query using v1 api instead
        # Code must be agnostic to system clock
        # instead, rely on prometheus clock

        # to get alerts
        # curl -g 'http://localhost:9090/api/v1/alerts'

        # to have all metrics:
        # curl -g 'http://localhost:9090/api/v1/label/__name__/values'\
        # {"status":"success","data":["ALERTS","ALERTS_FOR_STATE", ...]}

        # to get current time:
        # curl -g 'http://localhost:9090/api/v1/query?query=time()'
        # {"status":"success","data":{"resultType":"scalar","result":[1731134765.257,"1731134765.257"]}}

        # to get data for a given metric:
        # curl -g 'http://localhost:9090/api/v1/query_range?query=node:dev:disk_reads_rate1m&start=1731130861.241&end=1731134461.241&step=60'
        # where node:dev:disk_reads_rate1m is the metric,
        #       step=60                    is sample each 60s,
        #       end=1731134461.241         is the time now,
        #       start=1731130861.241       is an hour (600s) earlier.
        # {
        #     "status":"success",
        #     "data":{
        #                "resultType":"matrix",
        #                "result":[{"metric":{"__name__":"node:dev:disk_reads_rate1m","device":"sda","instance":"node_exporter:9100","job":"node_exporter"},"values":[[1731130861.241,"0.1101637668599871"],[1731130921.241,"6.10319007077649"],[1731130981.241,"0.12500000000000003"],[1731131221.241,"7.773037853954849"], ...]}]}}

        # In these pairs, first element is timestamp, second is value

        # To simplify, we keep a shortened set of metrics

        #     cpu_usage     ->     node:cpu:usage_avg1m
        #     disk_io       ->     node:cls:disk_io_bytes_rate1m
        #     disk_read     ->     node:cls:disk_read_bytes_rate1m
        #     disk_write    ->     node:cls:disk_write_bytes_rate1m
        #     mem_usage     ->     node:cls:mem_usage
        #     space_usage   ->     node:cls:space_usage

        # Register the actions available in this environment
        self.register_action(
            "whether_is_abnormal_metric",
            handler=self.whether_is_abnormal_metric_handler,
            description={
                "type": "function",
                "function": {
                    "name": "whether_is_abnormal_metric",
                    "description": "Check if a type of metric of the database system is abnormal or not using a staticical method. This is used for initial checking where has gone wrong.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_name": {
                                "type": "string",
                                "description": "The name of the metric to check for anormalies. It will examine the data from the last 10 minutes, sampling every second. Anomalies are checked using the KS test algorithm.",
                                "enum": [
                                    "cpu_usage",
                                    "memory_usage",
                                    "network_traffic",
                                    "io_activity"
                                ]
                            }
                        },
                        "required": ["metric_name"],
                        "additionalProperties": False
                    }
                }
            }
        )

        # RAG Enhanced
        self.register_action(
            "match_diagnose_knowledge",
            handler=self.match_diagnose_knowledge_handler,
            description={
                "type": "function",
                "function": {
                    "name": "match_diagnose_knowledge",
                    "description": "Check if a type of metric of the database system is abnormal or not using a staticical method across all related metrics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_name": {
                                "type": "string",
                                "description": "The type of metric to check for anormalies. It will examine the data from the last 10 minutes, sampling every second. Anomalies are checked using the KS test algorithm.",
                                "enum": [
                                    "cpu",
                                    "memory",
                                    "network",
                                    "io"
                                ]
                            }
                        },
                        "required": ["metric_name"],
                        "additionalProperties": False
                    }
                }
            }
        )

        # TODO: match_diagnose_knowledge, optimize_index_selection

    def whether_is_abnormal_metric_handler(self, metric_name: str) -> bool:
        #try:
        if True:
            # Get the metric data from Prometheus
            metric_name_mapped = allowed_metrics_full_names.get(metric_name, "")
            if metric_name_mapped == "":
                raise ValueError(f"Access to {metric_name} currently not supported")
                # yes, very easy to support, but too much metrics would overwhelm the llm
                # the real issue is to select important ones
            print(metric_name_mapped)
            values = get_prometheus_metric_data(metric_name_mapped)
            if not len(values):
                print('No values yet. Please wait at least 15s.')
                return False
            values_list = [float(v) for t, v in values]
            # Convert the list into a 1D NumPy array
            values_array = np.array(values_list)
            return detect_anomalies(values_array)
        #except Exception as e:
        #    print(f"Error fetching metric data: {e}")
        #    return False

    def match_diagnose_knowledge_handler(self, expert: str, metric_name: str) -> str:
        assert expert in ["ConfigurationExpert", "CpuExpert", "DiskExpert", "IndexExpert", "IoExpert", "MemoryExpert", "QueryExpert", "RecoveryExpert", "WorkloadExpert"]

        # first, we get the alert metrics
        # get alert
        alerts = self.get_alerts()
        # extract alert metric
        # {'alerts': [{'labels': {'alertname': 'NodeMemSwapped', 'category': 'node', 'instance': 'node_exporter:9100', 'job': 'node_exporter', 'level': '2', 'severity': 'INFO'}, 'annotations': {'description': 'node:ins:swap_usage[ins=] = 1.00 > 1%\n', 'summary': 'INFO NodeMemSwapped @node_exporter:9100 1.00'}, 'state': 'firing', 'activeAt': '2024-11-11T02:24:49.467858611Z', 'value': '9.996108979102929e-01'}]}
        # extract 'node:ins:swap_usage'
        alert_metrics = []
        alert_descriptions = []
        alert_metric_str = ""
        for alert in alerts['alerts']:
            alert_description = alert['annotations']['description']

            # Use regex to capture the metric name before the [ins=] part
            match = re.match(r'([a-zA-Z0-9:_]+)\[\]*\]', alert_description)

            alert_metric = alert_description.split('[')[0]
            alert_metrics.append(alert_metric.strip())  # Append cleaned metric name
            alert_descriptions.append(alert_description)

            alert_metric_str += f"{alert_metric.strip()} triggered alert: {alert_description}. \n"

            anomaly_data = get_prometheus_metric_data(alert_metric)
            anomaly_data_list = [float(v) for t, v in anomaly_data]
            anomaly_data_array = np.array(anomaly_data_list)
            anomaly_data_features = describe_data_features(anomaly_data_list)

            alert_metric_str += f"Data description for {alert_metric}: {anomaly_data_features} \n"
            alert_metric_str += f"\n"

        llm_selected_metric_str = ""
        assert metric_name in ["cpu", "memory", "network", "io"]

        for name in full_metrics_full_names[metric_name]:
            query = full_metrics_full_names[metric_name][name]
            data = get_prometheus_metric_data(query)
            data_list = [float(v) for t, v in data]
            data_array = np.array(data_list)
            anomaly = detect_anomalies(data_array)
            if anomaly[1]:
                data_features = describe_data_features(data_list)
                llm_selected_metric_str += f"{name} (Query: {query}) is abnormal.\n"
                llm_selected_metric_str += f"Data description: {data_features}\n"
                llm_selected_metric_str += f"\n"

        rag_str = f""
        self.kb.search(metric_name, expert=expert)
        rag_str += f"For expert {expert}, the following knowledge is matched: \n"

        # for 'description' in alert
        for alert_description in alert_descriptions:
            rag_str += f"For the alert description you wanted to look into, here are the matched knowledge: \n"
            for result in self.kb.search(alert_description, expert=expert, top_k=3):
                rag_str += f"{result}:\n"
                rag_str += f"Cause : {result['cause_name']}\n"
                rag_str += f"Metrics: {result['metrics']}\n"
                rag_str += f"Expert : {result['expert']}\n"
                rag_str += f"\n"

        # for metric proposed by llm
        rag_str += f"For the metric you wanted to look into, here are the matched knowledge: \n"
        for result in self.kb.search(llm_selected_metric_str, expert=expert, top_k=3):
            rag_str += f"{result}:\n"
            rag_str += f"Cause : {result['cause_name']}\n"
            rag_str += f"Metrics: {result['metrics']}\n"
            rag_str += f"Expert : {result['expert']}\n"
            rag_str += f"\n"

        return alert_metric_str + llm_selected_metric_str + rag_str

    def get_alerts(self) -> dict:
        prom_url = 'http://localhost:9090/api/v1/alerts'

        # Make the HTTP request to Prometheus
        response = requests.get(prom_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Extract the values (timestamp-value pairs) from the response
                return data['data']
            else:
                raise ValueError(f"Prometheus returned an error: {data.get('error', 'Unknown error')}")
        else:
            raise ValueError(f"Failed to query Prometheus. Status code: {response.status_code}")

    def terminate(self) -> None:
        subprocess.run(["docker", "compose", "down"], check=True)

if __name__ == "__main__":
    env = DBEnvironment(config={
        'environment': {
            'anomalies':
            [
                {
                    'anomaly': 'MISSING_INDEXES',
                    'threads': 1000,
                    'ncolumn': 1000,
                    'colsize': 1000,
                }
            ]
        }
    })
    while True:
        command = input('> ')
        if command == 'alert':
            print(env.get_alerts())
        elif command == 'cpu':
            print(env.whether_is_abnormal_metric_handler('cpu_usage'))
        elif command == 'analyze':
            print(env.match_diagnose_knowledge_handler('WorkloadExpert', 'cpu'))
        elif command == 'q':
            env.terminate()
            break
