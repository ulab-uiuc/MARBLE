import requests
import time

# Prometheus API URL
prometheus_api_url = "http://localhost:9090/api/v1/query"

# PromQL queries for CPU and memory usage
cpu_query = '100 - (avg by (instance) (irate(node_cpu_seconds_total{instance="node_exporter:9100",mode="idle"}[5m])) * 100)'
memory_query = '(node_memory_MemTotal_bytes{instance="node_exporter:9100"} - node_memory_MemAvailable_bytes{instance="node_exporter:9100"}) / node_memory_MemTotal_bytes{instance="node_exporter:9100"} * 100'

# Function to query Prometheus with retry logic
def query_prometheus(query, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(prometheus_api_url, params={'query': query}, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}, attempt {attempt + 1} of {retries}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}, attempt {attempt + 1} of {retries}")

        attempt += 1
        time.sleep(delay)
    return None  # Return None if all attempts fail

# Function to get CPU and memory usage with retry logic and error handling
def restart_decision(delay=1):
    while True:
        try:
            cpu_usage = query_prometheus(cpu_query)
            memory_usage = query_prometheus(memory_query)

            if cpu_usage and memory_usage:
                # Extract CPU usage value
                cpu_usage_value = cpu_usage['data']['result'][0]['value'][1]
                cpu = int(float(cpu_usage_value))

                # Extract memory usage value
                memory_usage_value = memory_usage['data']['result'][0]['value'][1]
                mem = int(float(memory_usage_value))

                # Print results
                print("CPU Usage:", cpu_usage_value, "%")
                print("Memory Usage:", memory_usage_value, "%")

                return cpu, mem
            else:
                print("Failed to retrieve metrics. Retrying...")

        except (KeyError, IndexError, ValueError) as e:
            print(f"Data extraction error: {e}. Retrying...")

        time.sleep(delay)

# Call the restart decision function
restart_decision()
