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
    def __init__(self):
        self.threats = deque(maxlen=100)  # Store the last 100 threats

    def analyze_traffic(self, traffic):
        """Analyze incoming and outgoing network traffic for threats."""
        for packet in traffic:
            if self.is_malicious(packet):
                threat = Threat(threat_type="Malware", source_ip=packet['source_ip'], severity="High")
                self.threats.append(threat)
                self.log_threat(threat)

    def is_malicious(self, packet):
        """Determine if a packet is malicious based on predefined patterns."""
        # Simulate threat detection logic
        return random.choice([True, False])  # Randomly simulating threat detection

    def log_threat(self, threat):
        """Log the detected threat."""
        logging.info(f"Threat detected: {threat.threat_type} from {threat.source_ip} with severity {threat.severity}")

class Dashboard:
    """User-friendly dashboard for displaying security alerts."""
    def __init__(self, detection_module):
        self.detection_module = detection_module

    def display_alerts(self):
        """Display real-time security alerts."""
        print("Real-time Security Alerts:")
        for threat in self.detection_module.threats:
            print(f"Type: {threat.threat_type}, Source IP: {threat.source_ip}, Severity: {threat.severity}")

class NetGuard:
    """Main class for the NetGuard security monitoring system."""
    def __init__(self):
        self.detection_module = ThreatDetectionModule()
        self.dashboard = Dashboard(self.detection_module)

    def run(self):
        """Run the NetGuard monitoring system."""
        while True:
            # Simulate incoming network traffic
            traffic = self.generate_traffic()
            self.detection_module.analyze_traffic(traffic)
            self.dashboard.display_alerts()
            time.sleep(5)  # Wait for 5 seconds before the next analysis

    def generate_traffic(self):
        """Generate simulated network traffic."""
        return [{'source_ip': f'192.168.1.{random.randint(1, 255)}'} for _ in range(10)]

if __name__ == "__main__":
    netguard = NetGuard()
    netguard.run()

# Test cases for the ThreatDetectionModule
# file_name_2.py
import unittest

class TestThreatDetectionModule(unittest.TestCase):
    def setUp(self):
        self.module = ThreatDetectionModule()

    def test_analyze_traffic_with_malware(self):
        """Test detection of malware in traffic."""
        traffic = [{'source_ip': '192.168.1.10'}]
        self.module.analyze_traffic(traffic)
        self.assertGreater(len(self.module.threats), 0)

    def test_analyze_traffic_without_malware(self):
        """Test no detection when traffic is benign."""
        traffic = [{'source_ip': '192.168.1.20'}]
        self.module.analyze_traffic(traffic)
        self.assertEqual(len(self.module.threats), 0)

if __name__ == "__main__":
    unittest.main()

# file_name_3.py
# Performance testing and edge case testing would typically be done in a separate script or testing framework.
# Here we can outline the approach for performance testing.

def performance_test():
    """Simulate heavy network traffic and measure performance."""
    detection_module = ThreatDetectionModule()
    start_time = time.time()
    
    # Simulate heavy traffic
    for _ in range(1000):  # Simulate 1000 packets
        traffic = [{'source_ip': f'192.168.1.{random.randint(1, 255)}'}]
        detection_module.analyze_traffic(traffic)
    
    end_time = time.time()
    print(f"Performance test completed in {end_time - start_time} seconds.")

if __name__ == "__main__":
    performance_test()