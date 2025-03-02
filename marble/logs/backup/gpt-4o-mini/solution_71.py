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
        self.is_running = True
        self.alerts = []
        self.logs = []
        self.suspicious_patterns = ["unauthorized_access", "data_exfiltration", "malware_signature"]
        self.monitor_thread = Thread(target=self.monitor_traffic)
        self.monitor_thread.start()

    def monitor_traffic(self):
        """ Continuously monitor network traffic for suspicious activities. """
        while self.is_running:
            # Simulate network traffic monitoring
            time.sleep(1)  # Simulate a delay for monitoring
            self.log_activity("Normal traffic detected.")
            if random.random() < 0.1:  # Simulate a 10% chance of suspicious activity
                self.detect_suspicious_activity()

    def detect_suspicious_activity(self):
        """ Detect suspicious activities and log alerts. """
        suspicious_activity = random.choice(self.suspicious_patterns)
        alert_message = f"Alert: Detected {suspicious_activity}."
        self.alerts.append(alert_message)
        self.log_activity(alert_message)

    def log_activity(self, message):
        """ Log activities and alerts. """
        logging.info(message)
        self.logs.append(message)

    def stop_monitoring(self):
        """ Stop the monitoring thread. """
        self.is_running = False
        self.monitor_thread.join()
        self.log_activity("Monitoring stopped.")

    def get_alerts(self):
        """ Retrieve current alerts. """
        return self.alerts

    def get_logs(self):
        """ Retrieve log entries. """
        return self.logs

# Test cases for NetworkGuard
def run_tests():
    """ Run test cases to validate NetworkGuard functionalities. """
    logging.info("Starting tests for NetworkGuard...")
    network_guard = NetworkGuard()
    
    # Allow some time for monitoring
    time.sleep(5)
    
    # Check alerts and logs
    alerts = network_guard.get_alerts()
    logs = network_guard.get_logs()
    
    # Validate outputs
    assert len(logs) > 0, "Logs should contain entries."
    assert len(alerts) >= 0, "Alerts should be retrievable."
    
    # Stop monitoring
    network_guard.stop_monitoring()
    logging.info("Tests completed.")

if __name__ == "__main__":
    run_tests()