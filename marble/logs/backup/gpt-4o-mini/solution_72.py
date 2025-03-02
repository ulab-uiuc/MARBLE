# solution.py

import random
import time
import logging
from collections import deque

# Configure logging for the application
logging.basicConfig(filename='netguard.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Threat:
    """Class representing a detected threat."""
    def __init__(self, threat_type, source_ip, severity):
        self.threat_type = threat_type
        self.source_ip = source_ip
        self.severity = severity

class ThreatDetectionModule:
    """Module for detecting threats in network traffic."""
    def __init__(self):def analyze_traffic(self, traffic):
        """Analyze incoming and outgoing network traffic for threats."""
        for packet in traffic:
            if self.is_malicious(packet):
                threat = Threat('Malicious', packet['source_ip'], 'High')
                self.log_threat(threat)
            elif self.is_phishing(packet):
                threat = Threat('Phishing', packet['source_ip'], 'Medium')
                self.log_threat(threat)
            elif self.is_unauthorized_access(packet):
                threat = Threat('Unauthorized Access', packet['source_ip'], 'High')
                self.log_threat(threat)    def log_threat(self, threat):
        """Log the detected threat."""
        self.threats.append(threat)
        logging.info(f'Detected {threat.threat_type} from {threat.source_ip} with severity {threat.severity}')

class Dashboard:
    """Dashboard for displaying security alerts."""
    def __init__(self, detection_module):
        self.detection_module = detection_module

    def display_alerts(self):
        """Display real-time security alerts."""
        print("Real-time Security Alerts:")
        for threat in self.detection_module.threats:
            print(f'Type: {threat.threat_type}, Source IP: {threat.source_ip}, Severity: {threat.severity}')

def simulate_network_traffic():
    """Simulate network traffic for testing purposes."""
    return [{'source_ip': f'192.168.1.{random.randint(1, 255)}'} for _ in range(10)]

def main():
    """Main function to run the NetGuard application."""
    detection_module = ThreatDetectionModule()
    dashboard = Dashboard(detection_module)

    # Simulate continuous network traffic monitoring
    while True:
        traffic = simulate_network_traffic()
        detection_module.analyze_traffic(traffic)
        dashboard.display_alerts()
        time.sleep(5)  # Wait for 5 seconds before the next traffic simulation

if __name__ == "__main__":
    main()