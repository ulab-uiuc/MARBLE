# network_guard.py

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List

# Define a logger for NetworkGuard
logger = logging.getLogger('NetworkGuard')
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('network_guard.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class NetworkTraffic:
    """Represents network traffic with source and destination IP addresses and ports."""

    def __init__(self, src_ip: str, src_port: int, dst_ip: str, dst_port: int):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    def __str__(self):
        return f"Source: {self.src_ip}:{self.src_port}, Destination: {self.dst_ip}:{self.dst_port}"


class NetworkGuard:
    """Monitors and analyzes network traffic for potential threats and unauthorized activities."""

    def __init__(self):
        self.traffic_log: List[NetworkTraffic] = []
        self.suspicious_traffic: List[NetworkTraffic] = []
        self.firewall_rules: Dict[str, int] = {}
        self.antivirus_signatures: Dict[str, str] = {}

    def monitor_traffic(self, traffic: NetworkTraffic):
        """Monitors incoming and outgoing network traffic and logs all activities."""
        self.traffic_log.append(traffic)
        logger.info(f"Traffic logged: {traffic}")

    def detect_suspicious_traffic(self, traffic: NetworkTraffic):
        """Detects and alerts on any suspicious activities."""
        if traffic.src_ip in self.firewall_rules and traffic.src_port == self.firewall_rules[traffic.src_ip]:
            self.suspicious_traffic.append(traffic)
            logger.warning(f"Suspicious traffic detected: {traffic}")
        elif traffic.dst_ip in self.antivirus_signatures and traffic.dst_port == self.antivirus_signatures[traffic.dst_ip]:
            self.suspicious_traffic.append(traffic)
            logger.warning(f"Suspicious traffic detected: {traffic}")

    def integrate_firewall(self, rules: Dict[str, int]):
        """Integrates with existing firewall solutions to enhance threat detection capabilities."""
        self.firewall_rules = rules
        logger.info("Firewall rules integrated")

    def integrate_antivirus(self, signatures: Dict[str, str]):
        """Integrates with existing antivirus solutions to enhance threat detection capabilities."""
        self.antivirus_signatures = signatures
        logger.info("Antivirus signatures integrated")

    def view_alerts(self):
        """Provides a user-friendly interface for administrators to view real-time alerts."""
        for traffic in self.suspicious_traffic:
            print(f"Suspicious traffic detected: {traffic}")

    def view_logs(self):
        """Provides a user-friendly interface for administrators to review logs."""
        for traffic in self.traffic_log:
            print(f"Traffic logged: {traffic}")


class NetworkGuardTest:
    """Comprehensive test cases for NetworkGuard."""

    def __init__(self):
        self.network_guard = NetworkGuard()

    def test_normal_traffic(self):
        """Tests normal network traffic."""
        traffic = NetworkTraffic("192.168.1.100", 80, "8.8.8.8", 80)
        self.network_guard.monitor_traffic(traffic)
        self.network_guard.detect_suspicious_traffic(traffic)
        self.network_guard.view_logs()

    def test_suspicious_traffic(self):
        """Tests suspicious network traffic."""
        traffic = NetworkTraffic("192.168.1.100", 8080, "8.8.8.8", 80)
        self.network_guard.integrate_firewall({"192.168.1.100": 8080})
        self.network_guard.monitor_traffic(traffic)
        self.network_guard.detect_suspicious_traffic(traffic)
        self.network_guard.view_alerts()

    def test_high_traffic_volume(self):
        """Tests high traffic volume."""
        for _ in range(1000):
            traffic = NetworkTraffic("192.168.1.100", 80, "8.8.8.8", 80)
            self.network_guard.monitor_traffic(traffic)
        self.network_guard.view_logs()

    def test_system_failure(self):
        """Tests system failure."""
        try:
            raise Exception("System failure")
        except Exception as e:
            logger.error(f"System failure: {e}")
        finally:
            self.network_guard.view_logs()


def main():
    network_guard_test = NetworkGuardTest()
    network_guard_test.test_normal_traffic()
    network_guard_test.test_suspicious_traffic()
    network_guard_test.test_high_traffic_volume()
    network_guard_test.test_system_failure()


if __name__ == "__main__":
    main()