import os
import subprocess
import time
from typing import Any, Dict, List

import numpy as np
import requests
from marble.environments.db_utils.anomaly_detection import detect_anomalies

from marble.environments.base_env import BaseEnvironment


def get_prometheus_metric_data(metric_name: str) -> List[Any]:
    """
    Query Prometheus for the given metric data from the last hour, sampling every 60 seconds.

    Args:
        metric_name (str): The name of the metric to retrieve (e.g., 'node:cpu:usage_avg1m').

    Returns:
        List[List[Any]]: A list of timestamp-value pairs for the metric over the past hour.
    """
    # Get the current time in Unix timestamp
    end_time = time.time()

    # Calculate the start time (one hour ago)
    start_time = end_time - 3600  # 3600 seconds = 1 hour

    # Prometheus query range URL
    prom_url = 'http://localhost:9090/api/v1/query_range'

    # Parameters for the query
    params = {
        'query': metric_name,
        'start': start_time,
        'end': end_time,
        'step': 60  # sample every 60 seconds
    }

    prom_url_with_params = f"{prom_url}?query={metric_name}&start={start_time}&end={end_time}&step=60"

    # Make the HTTP request to Prometheus
    response = requests.get(prom_url_with_params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            # Extract the values (timestamp-value pairs) from the response
            assert isinstance(data['data']['result'][0]['values'], list)
            return data['data']['result'][0]['values']
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

        # Register the actions available in this environment
        self.register_action(
            "whether_is_abnormal_metric",
            handler=self.whether_is_abnormal_metric_handler,
            description={
                "type": "function",
                "function": {
                    "name": "whether_is_abnormal_metric",
                    "description": "Check if an metric of the database system is abnormal or not.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_name": {
                                "type": "string",
                                "description": "The name of the metric to check for anormalies. It will examine the data from the last hour, sampling every 60 seconds. Anomalies are checked using the KS test algorithm.",
                                "enum": [
                                    "cpu_usage",
                                    "disk_io",
                                    "disk_read",
                                    "disk_write",
                                    "mem_usage",
                                    "space_usage"
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

    def whether_is_abnormal_metric_handler(self, metric_name: str) -> Dict[str, Any]:
        #try:
        if True:
            # Get the metric data from Prometheus
            metric_name_mapper = {
                "cpu_usage": "node:cpu:usage_avg1m",
                "disk_io":   "node:cls:disk_io_bytes_rate1m",
                "disk_read": "node:cls:disk_read_bytes_rate1m",
                "disk_write":"node:cls:disk_write_bytes_rate1m",
                "mem_usage": "node:cls:mem_usage",
                "space_usage": "node:cls:space_usage",
            }
            metric_name_mapped = metric_name_mapper.get(metric_name, "")
            if metric_name_mapped == "":
                raise ValueError(f"Access to {metric_name} currently not supported")
            print(metric_name_mapped)
            values = get_prometheus_metric_data(metric_name_mapped)
            if not len(values):
                print('No values yet. Please wait at least 15s.')
                return {"success": False, "message": "Execution failed. No values yet. Please wait at least 15s."}
            values_list = [float(v) for t, v in values]
            # Convert the list into a 1D NumPy array
            values_array = np.array(values_list, dtype=np.float64)
            ks_statistic, anomalies = detect_anomalies(values_array)
            if np.any(anomalies):
                print(f"Anomalies detected in the metric '{metric_name}'")
                return {"success": True, "message": f"Anomalies detected in the metric '{metric_name}'; ks_statistic: {ks_statistic}, anomalies: {anomalies}"}
            else:
                print(f"No anomalies detected in the metric '{metric_name}'")
                return {"success": True, "message": f"No anomalies detected in the metric '{metric_name}'"}

    def get_alerts(self) -> Dict[str, Any]:
        prom_url = 'http://localhost:9090/api/v1/alerts'

        # Make the HTTP request to Prometheus
        response = requests.get(prom_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Extract the values (timestamp-value pairs) from the response
                assert isinstance(data['data'], dict)
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
        elif command == 'q':
            env.terminate()
            break
