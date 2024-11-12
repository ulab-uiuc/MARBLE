import os
import subprocess
import time
from typing import Any, Dict, List
import re

import numpy as np
import requests
from marble.environments.db_utils.anomaly_detection import detect_anomalies, describe_data_features

from marble.environments.base_env import BaseEnvironment

from marble.environments.db_utils.metrics import allowed_metrics_full_names, full_metrics_full_names
from marble.environments.db_utils.diagnostic_kb import DiagnosticKB
from marble.environments.db_utils.slow_query import obtain_slow_queries

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
        'step': 1, # sample every second
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

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Starting Docker containers...")

        # Run docker-compose up in detached mode
        subprocess.run(["docker", "compose", "-f", os.path.join(self.current_dir, "db_env_docker", "docker-compose.yml"), "down", "-v"], shell=False, check=True)

        # Then, run "docker-compose up
        subprocess.run(["docker", "compose", "-f", os.path.join(self.current_dir, "db_env_docker", "docker-compose.yml"), "up", "-d", "--remove-orphans"], check=True)

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

        # Register the actions available in this environment
        self.register_action(
            "get_alerts",
            handler=self.get_alerts_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_alerts",
                    "description": "Get current alerts from the database monitoring system. Returns information about any active alerts including their names, descriptions, and severity levels.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False
                    }
                }
            }
        )

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
                            "expert": {
                                "type": "string",
                                "description": "The type of expert to consult",
                                "enum": [
                                    "ConfigurationExpert",
                                    "CpuExpert",
                                    "DiskExpert",
                                    "IndexExpert",
                                    "IoExpert",
                                    "MemoryExpert",
                                    "QueryExpert",
                                    "RecoveryExpert",
                                    "WorkloadExpert"
                                ]
                            },
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
                        "required": ["expert", "metric_name"],
                        "additionalProperties": False
                    }
                }
            }
        )

        is_initialized = False
        alerts = []
        while True:
            try:
                alerts = self.get_raw_alerts()['alerts']
                if len(alerts):
                    is_initialized = True
                    break
            except:
                pass
        print(f'Alert detected @ {alerts}')

    def get_alerts_handler(self) -> Dict[str, Any]:
        """
        Handler function to get current alerts from Prometheus.

        Returns:
            Dict[str, Any]: Dictionary containing alert information in a structured format
        """
        try:
            alerts = self.get_raw_alerts()
            formatted_alerts = []

            for alert in alerts.get('alerts', []):
                formatted_alert = {
                    'name': alert['labels'].get('alertname', 'Unknown'),
                    'severity': alert['labels'].get('severity', 'Unknown'),
                    'description': alert['annotations'].get('description', ''),
                    'state': alert.get('state', ''),
                    'active_since': alert.get('activeAt', ''),
                    'value': alert.get('value', '')
                }
                formatted_alerts.append(formatted_alert)

            return {
                'status': 'success',
                'alert_count': len(formatted_alerts),
                'alerts': formatted_alerts
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'alerts': []
            }

    def whether_is_abnormal_metric_handler(self, metric_name: str) -> bool:
        try:
            # Get the metric data from Prometheus
            metric_name_mapped = allowed_metrics_full_names.get(metric_name, "")
            if metric_name_mapped == "":
                raise ValueError(f"Access to {metric_name} currently not supported")
            print(metric_name_mapped)
            values = get_prometheus_metric_data(metric_name_mapped)
            if not len(values):
                print('No values yet. Please wait at least 15s.')
                return False
            values_list = [float(v) for t, v in values]
            # Convert the list into a 1D NumPy array
            values_array = np.array(values_list)
            return detect_anomalies(values_array)
        except Exception as e:
            print(f"Error fetching metric data: {e}")
            return False

    def match_diagnose_knowledge_handler(self, expert: str, metric_name: str) -> str:
        # first, we get the alert metrics
        alerts = self.get_raw_alerts()
        alert_metrics = []
        alert_descriptions = []
        alert_metric_str = ""
        for alert in alerts['alerts']:
            alert_description = alert['annotations']['description']
            alert_metric = alert_description.split('[')[0]
            alert_metrics.append(alert_metric.strip())
            alert_descriptions.append(alert_description)

            alert_metric_str += f"{alert_metric.strip()} triggered alert: {alert_description}. \n"

            anomaly_data = get_prometheus_metric_data(alert_metric)
            anomaly_data_list = [float(v) for t, v in anomaly_data]
            anomaly_data_array = np.array(anomaly_data_list)
            anomaly_data_features = describe_data_features(anomaly_data_list)

            alert_metric_str += f"Data description for {alert_metric}: {anomaly_data_features} \n"
            alert_metric_str += f"\n"

        llm_selected_metric_str = ""
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

        for alert_description in alert_descriptions:
            rag_str += f"For the alert description you wanted to look into, here are the matched knowledge: \n"
            for result in self.kb.search(alert_description, expert=expert, top_k=3):
                rag_str += f"{result}:\n"
                rag_str += f"Cause : {result['cause_name']}\n"
                rag_str += f"Metrics: {result['metrics']}\n"
                rag_str += f"Expert : {result['expert']}\n"
                rag_str += f"\n"

        slow_query_str = f"Here are the commands that took longest time:\n"
        slow_query_str += obtain_slow_queries()

        rag_str += f"For the metric you wanted to look into, here are the matched knowledge: \n"
        for result in self.kb.search(llm_selected_metric_str, expert=expert, top_k=3):
            rag_str += f"{result}:\n"
            rag_str += f"Cause : {result['cause_name']}\n"
            rag_str += f"Metrics: {result['metrics']}\n"
            rag_str += f"Expert : {result['expert']}\n"
            rag_str += f"\n"

        return alert_metric_str + llm_selected_metric_str + slow_query_str + rag_str

    def get_raw_alerts(self) -> dict:
        """
        Get raw alerts data from Prometheus.

        Returns:
            dict: Raw alerts data from Prometheus
        """
        prom_url = 'http://localhost:9090/api/v1/alerts'
        response = requests.get(prom_url)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data['data']
            else:
                raise ValueError(f"Prometheus returned an error: {data.get('error', 'Unknown error')}")
        else:
            raise ValueError(f"Failed to query Prometheus. Status code: {response.status_code}")

    def terminate(self) -> None:
        subprocess.run(["docker", "compose", "-f", os.path.join(self.current_dir, "db_env_docker", "docker-compose.yml"), "down"], check=True)

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
            print(env.get_alerts_handler())
        elif command == 'cpu':
            print(env.whether_is_abnormal_metric_handler('cpu_usage'))
        elif command == 'analyze':
            print(env.match_diagnose_knowledge_handler('WorkloadExpert', 'cpu'))
        elif command == 'slow':
            print(obtain_slow_queries())
        elif command == 'q':
            env.terminate()
            break
