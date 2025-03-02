# solution.py

import time
import random
import logging
from threading import Thread, Event

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkGuard:
    def __init__(self):
        # Initialize the monitoring system
        self.is_running = Event()
        self.is_running.set()
        self.log_file = "network_activity.log"
        self.suspicious_patterns = ["unauthorized_access", "data_exfiltration", "malware_signature"]
        self.alerts = []def monitor_traffic(self):
        """ Continuously monitor network traffic and log activities with rate management and error handling. """
        logging.info("NetworkGuard is now monitoring network traffic.")
        log_queue = []
        while self.is_running.is_set():
            try:
                # Simulate network traffic monitoring
                activity = self.simulate_network_activity()
                log_queue.append(activity)
                self.check_for_suspicious_activity(activity)
                if len(log_queue) >= 5:
                    self.batch_log_activity(log_queue)
                    log_queue.clear()
                time.sleep(1)  # Simulate a delay in monitoring
            except Exception as e:
                logging.error(f"Error during monitoring: {e}")
                time.sleep(5)  # Wait before retrying
        if log_queue:
            self.batch_log_activity(log_queue)  # Log any remaining activities

    def batch_log_activity(self, activities):
        """ Log a batch of network activities to a file. """
        with open(self.log_file, "a") as log:
            for activity in activities:
                log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Activity: {activity}\n"
                log.write(log_entry)
                logging.info(log_entry.strip())    def log_activity(self, activity):
        """ Log the network activity to a file. """
        with open(self.log_file, "a") as log:
            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Activity: {activity}\n"
            log.write(log_entry)
            logging.info(log_entry.strip())

    def check_for_suspicious_activity(self, activity):
        """ Check if the activity is suspicious and alert if necessary. """
        if activity in self.suspicious_patterns:if any(pattern in activity for pattern in self.suspicious_patterns):            alert_message = f"ALERT: Suspicious activity detected - {activity}"
            self.alerts.append(alert_message)
            logging.warning(alert_message)

    def stop_monitoring(self):
        """ Stop the monitoring process. """
        self.is_running.clear()
        logging.info("NetworkGuard has stopped monitoring network traffic.")

    def start(self):
        """ Start the monitoring in a separate thread. """
        monitoring_thread = Thread(target=self.monitor_traffic)
        monitoring_thread.start()
        return monitoring_thread

# Test cases for NetworkGuard
def run_tests():
    """ Run test cases to validate the functionality of NetworkGuard. """
    logging.info("Running test cases for NetworkGuard.")
    guard = NetworkGuard()
    guard.start()

    # Simulate running for a short period to gather logs and alerts
    time.sleep(10)
    guard.stop_monitoring()

    # Check the log file for entries
    with open(guard.log_file, "r") as log:
        logs = log.readlines()
        logging.info(f"Log entries: {len(logs)}")

    # Check for alerts
    if guard.alerts:
        logging.info(f"Alerts generated: {len(guard.alerts)}")
    else:
        logging.info("No alerts generated.")

if __name__ == "__main__":
    run_tests()