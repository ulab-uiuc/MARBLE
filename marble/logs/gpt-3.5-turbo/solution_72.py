# NetGuard - Security Monitoring System

class ThreatDetection:
    def __init__(self):
        self.detected_threats = []

    def analyze_network_traffic(self, traffic_data):
        # Implement threat detection algorithms here# Implement more sophisticated threat detection algorithms using pattern matching or machine learning to enhance accuracy and coverage            self.detected_threats.append({"type": "Suspicious Activity", "source_ip": traffic_data["source_ip"], "severity": "Medium"})

    def get_detected_threats(self):
        return self.detected_threats


class Dashboard:
    def __init__(self):
        self.security_alerts = []

    def display_alert(self, threat):
        # Display real-time security alerts on the dashboard
        self.security_alerts.append(threat)
        print("Security Alert - Type: {}, Source IP: {}, Severity: {}".format(threat["type"], threat["source_ip"], threat["severity"]))


class LoggingSystem:
    def __init__(self):
        self.log = []

    def log_event(self, event):
        # Log detected threats and user actions for historical analysis and compliance reporting
        self.log.append(event)
        print("Event logged: {}".format(event))


# Test cases
def run_test_cases():
    threat_detector = ThreatDetection()
    dashboard = Dashboard()
    logger = LoggingSystem()

    # Test case 1: Malware detected
    traffic_data_1 = {"source_ip": "192.168.1.1", "malware": True}
    threat_detector.analyze_network_traffic(traffic_data_1)
    threats = threat_detector.get_detected_threats()
    for threat in threats:
        dashboard.display_alert(threat)
        logger.log_event(threat)

    # Test case 2: Phishing attempt detected
    traffic_data_2 = {"source_ip": "192.168.1.2", "phishing": True}
    threat_detector.analyze_network_traffic(traffic_data_2)
    threats = threat_detector.get_detected_threats()
    for threat in threats:
        dashboard.display_alert(threat)
        logger.log_event(threat)

    # Test case 3: Unauthorized access detected
    traffic_data_3 = {"source_ip": "192.168.1.3", "unauthorized_access": True}
    threat_detector.analyze_network_traffic(traffic_data_3)
    threats = threat_detector.get_detected_threats()
    for threat in threats:
        dashboard.display_alert(threat)
        logger.log_event(threat)


if __name__ == "__main__":
    run_test_cases()