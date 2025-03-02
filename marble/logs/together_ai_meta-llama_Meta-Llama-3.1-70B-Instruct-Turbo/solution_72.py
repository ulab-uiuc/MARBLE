# netguard.py

import logging
import threading
import time
from datetime import datetime
from random import randint

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetGuard:
    def __init__(self):
        self.threats = []
        self.lock = threading.Lock()

    def detect_threats(self, network_traffic):
        # Simulate threat detection algorithm
        threats = []
        for packet in network_traffic:
            if packet['source_ip'] == '192.168.1.100' or packet['destination_ip'] == '192.168.1.100':
                threats.append({
                    'type': 'Malware',
                    'source_ip': packet['source_ip'],
                    'destination_ip': packet['destination_ip'],
                    'severity': 'High'
                })
            elif packet['source_port'] == 80 or packet['destination_port'] == 80:
                threats.append({
                    'type': 'Phishing Attempt',
                    'source_ip': packet['source_ip'],
                    'destination_ip': packet['destination_ip'],
                    'severity': 'Medium'
                })
            elif packet['protocol'] == 'TCP' and packet['source_port'] == 22:
                threats.append({
                    'type': 'Unauthorized Access',
                    'source_ip': packet['source_ip'],
                    'destination_ip': packet['destination_ip'],
                    'severity': 'High'
                })
        return threats

    def log_threats(self, threats):
        with self.lock:
            for threat in threats:
                logging.info(f"Detected threat: {threat['type']} from {threat['source_ip']} to {threat['destination_ip']} with severity {threat['severity']}")
                self.threats.append(threat)

    def display_dashboard(self):
        while True:
            with self.lock:
                print("NetGuard Dashboard:")
                for threat in self.threats:
                    print(f"Type: {threat['type']}, Source IP: {threat['source_ip']}, Destination IP: {threat['destination_ip']}, Severity: {threat['severity']}")
            time.sleep(1)

    def start(self):
        # Simulate network traffic
        network_traffic = [
            {'source_ip': '192.168.1.100', 'destination_ip': '8.8.8.8', 'source_port': 1234, 'destination_port': 80, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.101', 'destination_ip': '8.8.8.8', 'source_port': 80, 'destination_port': 1234, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.102', 'destination_ip': '8.8.8.8', 'source_port': 22, 'destination_port': 22, 'protocol': 'TCP'}
        ]

        # Start threat detection thread
        threat_detection_thread = threading.Thread(target=self.detect_and_log_threats, args=(network_traffic,))
        threat_detection_thread.start()

        # Start dashboard thread
        dashboard_thread = threading.Thread(target=self.display_dashboard)
        dashboard_thread.start()

    def detect_and_log_threats(self, network_traffic):
        while True:
            threats = self.detect_threats(network_traffic)
            self.log_threats(threats)
            time.sleep(1)

if __name__ == "__main__":
    netguard = NetGuard()
    netguard.start()

# test_netguard.py

import unittest
from netguard import NetGuard

class TestNetGuard(unittest.TestCase):
    def test_detect_threats(self):
        netguard = NetGuard()
        network_traffic = [
            {'source_ip': '192.168.1.100', 'destination_ip': '8.8.8.8', 'source_port': 1234, 'destination_port': 80, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.101', 'destination_ip': '8.8.8.8', 'source_port': 80, 'destination_port': 1234, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.102', 'destination_ip': '8.8.8.8', 'source_port': 22, 'destination_port': 22, 'protocol': 'TCP'}
        ]
        threats = netguard.detect_threats(network_traffic)
        self.assertEqual(len(threats), 3)

    def test_log_threats(self):
        netguard = NetGuard()
        threats = [
            {'type': 'Malware', 'source_ip': '192.168.1.100', 'destination_ip': '8.8.8.8', 'severity': 'High'},
            {'type': 'Phishing Attempt', 'source_ip': '192.168.1.101', 'destination_ip': '8.8.8.8', 'severity': 'Medium'},
            {'type': 'Unauthorized Access', 'source_ip': '192.168.1.102', 'destination_ip': '8.8.8.8', 'severity': 'High'}
        ]
        netguard.log_threats(threats)
        self.assertEqual(len(netguard.threats), 3)

if __name__ == "__main__":
    unittest.main()

# performance_test_netguard.py

import time
import unittest
from netguard import NetGuard

class TestNetGuardPerformance(unittest.TestCase):
    def test_performance(self):
        netguard = NetGuard()
        network_traffic = [
            {'source_ip': '192.168.1.100', 'destination_ip': '8.8.8.8', 'source_port': 1234, 'destination_port': 80, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.101', 'destination_ip': '8.8.8.8', 'source_port': 80, 'destination_port': 1234, 'protocol': 'TCP'},
            {'source_ip': '192.168.1.102', 'destination_ip': '8.8.8.8', 'source_port': 22, 'destination_port': 22, 'protocol': 'TCP'}
        ]
        start_time = time.time()
        for _ in range(1000):
            netguard.detect_threats(network_traffic)
        end_time = time.time()
        self.assertLess(end_time - start_time, 1)

if __name__ == "__main__":
    unittest.main()

# edge_case_test_netguard.py

import unittest
from netguard import NetGuard

class TestNetGuardEdgeCases(unittest.TestCase):
    def test_known_secure_source(self):
        netguard = NetGuard()
        network_traffic = [
            {'source_ip': '8.8.8.8', 'destination_ip': '192.168.1.100', 'source_port': 80, 'destination_port': 1234, 'protocol': 'TCP'}
        ]
        threats = netguard.detect_threats(network_traffic)
        self.assertEqual(len(threats), 0)

    def test_encrypted_traffic(self):
        netguard = NetGuard()
        network_traffic = [
            {'source_ip': '192.168.1.100', 'destination_ip': '8.8.8.8', 'source_port': 443, 'destination_port': 443, 'protocol': 'TCP'}
        ]
        threats = netguard.detect_threats(network_traffic)
        self.assertEqual(len(threats), 0)

if __name__ == "__main__":
    unittest.main()