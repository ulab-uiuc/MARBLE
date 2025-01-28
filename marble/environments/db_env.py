import os
import re
import subprocess
import time
from typing import Any, Dict, List

import numpy as np
import psycopg2
import requests
from psycopg2 import OperationalError

from marble.environments.base_env import BaseEnvironment
from marble.environments.db_utils.anomaly_detection import (
    describe_data_features,
    detect_anomalies,
)
from marble.environments.db_utils.diagnostic_kb import DiagnosticKB
from marble.environments.db_utils.metrics import full_metrics_full_names
from marble.environments.db_utils.slow_query import obtain_slow_queries


def split_sql_statements(sql: str) -> List[str]:
    statements = re.split(r';\s*\n', sql)
    return [stmt.strip() for stmt in statements if stmt.strip()]

def get_prometheus_metric_data(metric_name: str, start_time: float, end_time: float, step: int = 1) -> List[List[Any]]:
    prom_url = 'http://localhost:9090/api/v1/query_range'
    params = {
        'query': metric_name,
        'start': start_time,
        'end': end_time,
        'step': step,
    }
    response = requests.get(prom_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            try:
                return data['data']['result'][0]['values']
            except Exception:
                return []
        else:
            raise ValueError(f"Prometheus returned an error: {data.get('error', 'Unknown error')}")
    else:
        raise ValueError(f"Failed to query Prometheus. Status code: {response.status_code}")

def get_current_time() -> float:
    return time.time()

def get_metric_data_for_last_10_minutes(metric_name: str) -> List[List[Any]]:
    end_time = get_current_time()
    start_time = end_time - 600
    return get_prometheus_metric_data(metric_name, start_time, end_time)

class DBEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str = "DBEnv"):
        super().__init__(name, config)
        self.kb = DiagnosticKB()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.start_docker_containers()
        self.initialize_database(config)
        self.register_actions()
        self.wait_for_alerts()
        # self.get_rag_handler('WorkloadExpert', 'cpu')
        # self.get_slow_query_handler()
        # print out results from each handler as a test
        print(self.get_alerts_handler())
        print(self.get_alert_metrics_handler())
        print(self.detect_metric_abnormality_handler('cpu'))
        print(self.get_rag_handler('WorkloadExpert', 'cpu'))
        print(self.get_slow_query_handler())

    def start_docker_containers(self):
        print("Starting Docker containers...")
        subprocess.run(["sudo", "docker", "compose", "down", "-v"], cwd=os.path.join(self.current_dir, "db_env_docker"), shell=False, check=True)
        subprocess.run(["sudo", "docker", "compose", "up", "-d", "--remove-orphans"], cwd=os.path.join(self.current_dir, "db_env_docker"), check=True)

    def initialize_database(self, config: Dict[str, Any]):
        while not self.check_db_connection():
            time.sleep(1)

        init_sql = config.get('init_sql', None)
        test_sql = config.get('test_sql', None)

        connection = psycopg2.connect(
            user="test",
            password="Test123_456",
            database="sysbench",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        connection.autocommit = True
        cursor.execute("SET client_min_messages TO WARNING;")
        print("Warning messages turned off.")

        print("Initializing the database...")
        if init_sql is not None and len(init_sql):
            for statement in split_sql_statements(init_sql):
                cursor.execute(statement)
        else:
            print("No init SQL statements provided. Skipping...")

        cursor.execute("RESET client_min_messages;")
        print("Warning messages turned on.")

        cursor.execute("CREATE EXTENSION pg_stat_statements;")

        # interactive sql shell
        # while True:
        #     sql = input("Enter SQL statement: ")
        #     if sql == 'q':
        #         break
        #     try:
        #         cursor.execute(sql)
        #         print(cursor.fetchall())
        #     except Exception as e:
        #         print(f"Error executing SQL statement: {e}")

        print("pg_stat_statements extension created.")

        print("Executing test SQL statements...")

        anomalies = config.get('anomalies', [])
        if anomalies:
            for anomaly in anomalies:
                anomaly_type = anomaly['anomaly']
                threads = anomaly['threads']
                ncolumn = anomaly['ncolumn']
                colsize = anomaly['colsize']
                subprocess.run(["python", "main.py", "--anomaly", anomaly_type, "--threads", f"{threads}", "--ncolumn", f"{ncolumn}", "--colsize", f"{colsize}"], cwd=os.path.join(self.current_dir, "db_env_docker", "anomaly_trigger"), check=True)
        else:
            print(
                (
                    "*** WARNING ***\n"
                    "This is an experimental feature.\n"
                    "Generally, it is difficult for one single SQL query\n"
                    "to trigger an alarm. Please be careful in designing\n"
                    "the test SQL queries, or the experiment will take forever\n"
                    "waiting for an alarm to be triggered."
                )
            )
            for statement in split_sql_statements(test_sql):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Error executing SQL statement: {e}")

    def register_actions(self) -> None:
        # self.register_action(
        #     "get_alerts",
        #     handler=self.get_alerts_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "get_alerts",
        #             "description": "Get current alerts from the database monitoring system. Returns information about any active alerts including their names, descriptions, and severity levels.",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {},
        #                 "required": [],
        #                 "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        # self.register_action(
        #     "get_alert_metrics",
        #     handler=self.get_alert_metrics_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "get_alert_metrics",
        #             "description": "Get metrics related to current alerts from the database monitoring system.",
        #             "parameters": {
        #             "type": "object",
        #             "properties": {},
        #             "required": [],
        #             "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        # self.register_action(
        #     "detect_metric_abnormality",
        #     handler=self.detect_metric_abnormality_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "detect_metric_abnormality",
        #             "description": "Get detailed information about a specific metric selected by the LLM.",
        #             "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "metric_name": {
        #                     "type": "string",
        #                     "description": "The name of the metric to get information about.",
        #                     "enum": [
        #                         "cpu",
        #                         "memory",
        #                         "network",
        #                         "io"
        #                     ]
        #                 }
        #             },
        #             "required": ["metric_name"],
        #             "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        # self.register_action(
        #     "get_rag",
        #     handler=self.get_rag_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "get_rag",
        #             "description": "Get relevant knowledge from the RAG system based on the expert and metric name.",
        #             "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "expert": {
        #                     "type": "string",
        #                     "description": "The type of expert to consult. Please input the one matching with your profession.",
        #                     "enum": [
        #                         "ConfigurationExpert",
        #                         "CpuExpert",
        #                         "DiskExpert",
        #                         "IndexExpert",
        #                         "IoExpert",
        #                         "MemoryExpert",
        #                         "QueryExpert",
        #                         "RecoveryExpert",
        #                         "WorkloadExpert"
        #                     ]
        #                 },
        #                 "query_str": {
        #                     "type": "string",
        #                     "description": "What you would like to find the root cause for."
        #                 }
        #             },
        #             "required": ["expert", "metric_name", "llm_selected_metric_str"],
        #             "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        # self.register_action(
        #     "get_slow_query",
        #     handler=self.get_slow_query_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "get_slow_query",
        #             "description": "Get information about the slowest queries executed in the database.",
        #             "parameters": {
        #             "type": "object",
        #             "properties": {},
        #             "required": [],
        #             "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        # self.register_action(
        #     'get_docker_postgresql_error_query_log',
        #     handler=self.get_docker_postgresql_error_query_log_handler,
        #     description={
        #         "type": "function",
        #         "function": {
        #             "name": "get_docker_postgresql_error_query_log",
        #             "description": "Get the last 100 lines of the PostgreSQL query error log.",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {},
        #                 "required": [],
        #                 "additionalProperties": False
        #             }
        #         }
        #     }
        # )

        self.register_action(
            'query_db',
            handler=self.query_db_handler,
            description={
                "type": "function",
                "function": {
                    "name": "query_db",
                    "description": (
                        "Query the PostgreSQL database with the given SQL statement. \n"
                        "Please keep to the pg_stat_statements "
                        "table, and make sure that your query itself "
                        "won't cause the database to hang. \n"
                        "Recommended to use one single query at a time. \n"
                        "You will get the result of the query."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": (
                                    "The SQL statement to execute. \n"
                                    "You can try to access these tables: \n"
                                    "For insert related: \n"
                                    "- pg_stat_queries, for running queries \n"
                                    "- pg_stat_statements, for detailed query statistics \n"
                                    "For lock contention related: \n"
                                    "- pg_locks, for lock waits and contention \n"
                                    "- pg_stat_activity, for identifying blocked and active queries \n"
                                    "For redundant indexes: \n"
                                    "- pg_indexes, for index definitions \n"
                                    "- pg_stat_user_indexes, for index usage statistics \n"
                                    "For vacuum related: \n"
                                    "- pg_stat_all_tables, forvdetailed statistics about vacuuming, auto vacuuming, "
                                    "and analyze operations for each table \n"
                                    "For example, here is how you can get the slowest "
                                    "queries: \n"
                                    "SELECT query, total_exec_time \n"
                                    "FROM pg_stat_statements \n"
                                    "ORDER BY total_exec_time DESC \n"
                                    "LIMIT 10;\n\n"
                                    "Here is how you can get slowest SELECT data fetching queries: \n"
                                    "SELECT query, total_exec_time \n"
                                    "FROM pg_stat_statements \n"
                                    "WHERE query LIKE 'SELECT%' \n"
                                    "ORDER BY total_exec_time DESC \n"
                                    "LIMIT 10;\n\n"
                                    "It is advised you don't query with limit set "
                                    "way too high, like not more than 100. "
                                    "Only include query statements in this param."
                                )
                            }
                        },
                        "required": ["sql"],
                        "additionalProperties": False
                    }
                }
            }
        )

    def wait_for_alerts(self) -> None:
        return True
        # is_initialized = False
        # alerts = []
        # time_before_alert_detection = time.time()
        # time_last_print = time.time()
        # while True:
        #     try:
        #         alerts = self.get_raw_alerts()['alerts']
        #         time_now = time.time()
        #         if time_now - time_before_alert_detection > 1:
        #             time_before_alert_detection = time_now
        #             print(f'Waited time: {time.strftime("%H:%M:%S", time.gmtime(time_now - time_last_print))}', end='\r')

        #         if len(alerts):
        #             is_initialized = True
        #             break
        #     except:
        #         pass
        # print(f'Alert detected @ {alerts}')

    def get_docker_postgresql_error_query_log_handler(self) -> Dict[str, Any]:
        raise Exception("This function is STILL IN DEVELOPMENT. Please try again later.")
        # use a command
        result = os.popen("sudo docker logs -tf db_env_docker-postgres_db-1").read()
        # get last 100 lines and make it string
        result = '\n'.join(result.split('\n')[-100:])
        if result:
            return {
                'status': 'success',
                'function_name': 'get_docker_postgresql_error_query_log',
                'explanation': (
                    "Here are the last 100 lines of the PostgreSQL query error log: \n"
                    f"{result}"
                )
            }
        else:
            return {
                'status': 'success',
                'function_name': 'get_docker_postgresql_error_query_log',
                'explanation': "No failed queries found in the PostgreSQL query error log."
            }

    def get_alerts_handler(self) -> Dict[str, Any]:
        try:
            alerts = self.get_raw_alerts()
            formatted_alerts = []

            for alert in alerts.get('alerts', []):
                formatted_alert = {
                    'function_name': 'get_alerts',
                    'name': alert['labels'].get('alertname', 'Unknown'),
                    'severity': alert['labels'].get('severity', 'Unknown'),
                    'description': alert['annotations'].get('description', ''),
                    'state': alert.get('state', ''),
                    'active_since': alert.get('activeAt', ''),
                    'value': alert.get('value', '')
                }
                formatted_alerts.append(formatted_alert)

            explanation = ''
            for alert in formatted_alerts:
                explanation += f"{alert['name']} triggered alert: {alert['description']}. \n"
                explanation += f"Severity: {alert['severity']}. \n"
                explanation += f"State: {alert['state']}. \n"
                explanation += f"Active since: {alert['active_since']}. \n"
                explanation += f"Value: {alert['value']}. \n\n"

            return {
                'status': 'success',
                'alert_count': len(formatted_alerts),
                # 'alerts': formatted_alerts,
                'explanation': explanation
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                # 'alerts': [],
                'explanation': 'No alerts found now. You can try again later.'
            }

    def get_alert_metrics_handler(self) -> Dict[str, Any]:
        try:
            alert_metrics_str = self.get_alert_metrics_str()
            return {
                'status': 'success',
                'function_name': 'get_alert_metrics',
                'explanation': alert_metrics_str
            }
        except Exception as e:
            return {
                'status': 'error',
                'function_name': 'get_alert_metrics',
                'explanation': str(e)
            }

    def detect_metric_abnormality_handler(self, metric_name: str) -> Dict[str, Any]:
        try:
            llm_selected_metric_str = self.detect_metric_abnormality_str(metric_name)
            return {
                'status': 'success',
                'function_name': 'detect_metric_abnormality',
                'explanation': llm_selected_metric_str
            }
        except Exception as e:
            return {
                'status': 'error',
                'function_name': 'detect_metric_abnormality',
                'explanation': str(e)
            }

    def get_rag_handler(self, expert: str, query_str: str) -> Dict[str, Any]:
        try:
            rag_str = self.get_rag_str(expert, query_str)
            return {
                'status': 'success',
                'function_name': 'get_rag',
                'explanation': rag_str
            }
        except Exception as e:
            return {
                'status': 'error',
                'function_name': 'get_rag',
                'explanation': str(e)
            }

    def query_db_handler(self, sql: str) -> Dict[str, Any]:
        try:
            connection = psycopg2.connect(
                user="test",
                password="Test123_456",
                database="sysbench",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
            sql_queries = split_sql_statements(sql)
            for sql_query in sql_queries:
                cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            return {
                'status': 'success',
                'function_name': 'query_db',
                'explanation': f"Your query on the database was successful{'' if len(result) else ' but no data was returned'}. \nYour query is: {sql_queries} \nResult: {result}"
            }
        except Exception as e:
            return {
                'status': 'error',
                'function_name': 'query_db',
                'explanation': f"An error occurred while you tried to query the database: {str(e)}"
            }

    def get_slow_query_handler(self) -> Dict[str, Any]:
        try:
            slow_query_str = self.get_slow_query_str()
            return {
                'status': 'success',
                'function_name': 'get_slow_query',
                'explanation': slow_query_str
            }
        except Exception as e:
            return {
                'status': 'error',
                'function_name': 'get_slow_query',
                'explanation': str(e)
            }

    def get_alert_metrics_str(self) -> Dict[str, Any]:
        alerts = self.get_raw_alerts()
        alert_metrics_str = ""
        for alert in alerts['alerts']:
            alert_description = alert['annotations']['description']
            alert_metric = alert_description.split('[')[0]
            alert_metrics_str += f"{alert_metric.strip()} triggered alert: {alert_description}. \n"
            anomaly_data = get_metric_data_for_last_10_minutes(alert_metric)
            anomaly_data_list = [float(v) for t, v in anomaly_data]
            anomaly_data_features = describe_data_features(anomaly_data_list)
            alert_metrics_str += f"Data description for {alert_metric}: {anomaly_data_features} \n\n"
        return {
            'status': 'success',
            'function_name': 'get_alert_metrics',
            'explanation': alert_metrics_str
        }

    def detect_metric_abnormality_str(self, metric_name: str) -> Dict[str, Any]:
        llm_selected_metric_str = ""
        for name in full_metrics_full_names[metric_name]:
            query = full_metrics_full_names[metric_name][name]
            data = get_metric_data_for_last_10_minutes(query)
            data_list = [float(v) for t, v in data]
            if not len(data_list):
                llm_selected_metric_str += f"No data found for {name} (Query: {query}).\n"
                llm_selected_metric_str += "Please wait at least 15s.\n\n"
                continue
            data_array = np.array(data_list)
            anomaly = detect_anomalies(data_array)
            if anomaly['anomalies']:
                data_features = describe_data_features(data_list)
                llm_selected_metric_str += f"{name} (Query: {query}) is abnormal.\n"
                llm_selected_metric_str += f"Data description: {data_features}\n\n"
        return {
            'status': 'success',
            'function_name': 'detect_metric_abnormality',
            'explanation': llm_selected_metric_str
        }

    def get_rag_str(self, expert: str, llm_selected_metric_str: str) -> Dict[str, Any]:
        rag_str = f"For expert {expert}, the following knowledge is matched: \n"
        for result in self.kb.search(llm_selected_metric_str, expert=expert):
            rag_str += f"{result}:\n"
            rag_str += f"Cause : {result['cause_name']}\n"
            rag_str += f"Metrics: {result['metrics']}\n"
            rag_str += f"Expert : {result['expert']}\n\n"
        return {
            'status': 'success',
            'function_name': 'get_rag',
            'explanation': rag_str
        }

    def get_slow_query_str(self) -> str:
        return f"Here are the commands that took longest time:\n{obtain_slow_queries()}"

    def get_raw_alerts(self) -> dict:
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

    def check_db_connection(self) -> bool:
        try:
            connection = psycopg2.connect(
                user="test",
                password="Test123_456",
                database="sysbench",
                host="localhost",
                port="5432"
            )
            print("Database is up!")
            connection.close()
            return True
        except OperationalError:
            print("Database is not available.")
            return False

    def terminate(self) -> None:
        subprocess.run(["sudo", "docker", "compose", "down"], cwd=os.path.join(self.current_dir, "db_env_docker"), check=True)

if __name__ == "__main__":
    raise NotImplementedError("This demo is obsolete. Please run the experiment directly.")
    env = DBEnvironment(config={
        'environment': {
            'anomalies': [
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
            print(env.detect_metric_abnormality_handler('cpu_usage'))
        elif command == 'analyze':
            print(env.match_diagnose_knowledge_handler('WorkloadExpert', 'cpu'))
        elif command == 'slow':
            print(obtain_slow_queries())
        elif command == 'q':
            env.terminate()
            break
