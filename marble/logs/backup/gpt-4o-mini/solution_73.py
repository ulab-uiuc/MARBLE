# solution.py

import logging
import random
import time
from cryptography.fernet import Fernet
from sklearn.ensemble import IsolationForest
import numpy as np

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Real-time monitoring module
class RealTimeMonitor:
    def __init__(self):
        self.logs = []  # List to store logs of network activity

    def log_activity(self, activity):
        """Log network activity."""
        self.logs.append(activity)
        logging.info(f"Activity logged: {activity}")

    def display_logs(self):
        """Display all logged activities."""
        for log in self.logs:
            print(log)

# Threat detection module using machine learning
class ThreatDetector:
    def __init__(self):
        self.model = IsolationForest()  # Using Isolation Forest for anomaly detection

    def train_model(self, data):
        """Train the threat detection model on historical data."""
        self.model.fit(data)

    def detect_threats(self, data):
        """Detect threats in the incoming data."""
        predictions = self.model.predict(data)        if not data or not isinstance(data, (list, np.ndarray)):
            logging.error("Invalid input data: must be a non-empty list or numpy array.")
            return []
        predictions = self.model.predict(data)        if not data or not isinstance(data, (list, np.ndarray)):
            logging.error("Invalid input data: must be a non-empty list or numpy array.")
            return []
        predictions = self.model.predict(data)        threats = [data[i] for i in range(len(predictions)) if predictions[i] == -1]
        return threats

# Secure data management module
class SecureDataManager:
    def __init__(self):
        self.key = Fernet.generate_key()  # Generate a key for encryption
        self.cipher = Fernet(self.key)  # Create a cipher object

    def encrypt_data(self, data):
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_data).decode()

# Main application class
class SecureNet:
    def __init__(self):
        self.monitor = RealTimeMonitor()
        self.detector = ThreatDetector()
        self.data_manager = SecureDataManager()

    def simulate_network_activity(self):
        """Simulate network activity for monitoring and threat detection."""
        for _ in range(10):
            activity = f"User accessed resource {random.randint(1, 100)}"
            self.monitor.log_activity(activity)
            time.sleep(0.5)  # Simulate time delay between activities

    def simulate_threat_detection(self):
        """Simulate threat detection with random data."""
        # Generate random data for training and detection
        normal_data = np.random.normal(0, 1, (100, 1))
        self.detector.train_model(normal_data)

        # Simulate incoming data with some anomalies
        incoming_data = np.random.normal(0, 1, (20, 1)).tolist() + [[10], [-10]]  # Adding anomalies
        threats = self.detector.detect_threats(incoming_data)
        if threats:
            logging.warning(f"Threats detected: {threats}")
        else:
            logging.info("No threats detected.")

    def secure_data_example(self):
        """Example of secure data management."""
        sensitive_data = "This is sensitive information."
        encrypted_data = self.data_manager.encrypt_data(sensitive_data)
        logging.info(f"Encrypted data: {encrypted_data}")

        decrypted_data = self.data_manager.decrypt_data(encrypted_data)
        logging.info(f"Decrypted data: {decrypted_data}")

# Test cases to validate functionality
def run_tests():
    logging.info("Running tests...")

    # Test real-time monitoring
    monitor = RealTimeMonitor()
    monitor.log_activity("Test activity 1")
    monitor.log_activity("Test activity 2")
    assert len(monitor.logs) == 2, "Real-time monitoring test failed."

    # Test threat detection
    detector = ThreatDetector()
    normal_data = np.random.normal(0, 1, (100, 1))
    detector.train_model(normal_data)
    incoming_data = np.random.normal(0, 1, (20, 1)).tolist() + [[10], [-10]]
    threats = detector.detect_threats(incoming_data)
    assert len(threats) == 2, "Threat detection test failed."

    # Test secure data management
    data_manager = SecureDataManager()
    sensitive_data = "Sensitive data"
    encrypted_data = data_manager.encrypt_data(sensitive_data)
    decrypted_data = data_manager.decrypt_data(encrypted_data)
    assert sensitive_data == decrypted_data, "Secure data management test failed."

    logging.info("All tests passed.")

if __name__ == "__main__":
    secure_net = SecureNet()
    secure_net.simulate_network_activity()
    secure_net.simulate_threat_detection()
    secure_net.secure_data_example()
    run_tests()