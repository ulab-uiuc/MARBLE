class NetworkGuard:
    def __init__(self):
        self.log = []  # Initialize an empty log to store network activities

    def monitor_traffic(self, traffic):
        """
        Monitor incoming and outgoing network traffic.
        Log all activities and detect suspicious patterns.
        """
        self.log.append(traffic)  # Log the network traffic

        # Implement detection logic for suspicious activities
        if "unauthorized access" in traffic:
            self.alert("Unauthorized access attempt detected!")
        elif "unusual data transfer" in traffic:
            self.alert("Unusual data transfer pattern detected!")
        elif "malware signature" in traffic:
            self.alert("Known malware or virus signature detected!")

    def alert(self, message):
        """
        Generate an alert for suspicious activities.
        This can be extended to send notifications to administrators.
        """
        print("ALERT: " + message)

    def view_logs(self):
        """
        Display the log of network activities for administrators to review.
        """
        for activity in self.log:
            print(activity)

# Test casesimport unittest

class TestNetworkGuard(unittest.TestCase):

    def test_normal_traffic(self):
        ng = NetworkGuard()
        ng.monitor_traffic("Normal traffic from user A to server")
        ng.monitor_traffic("Normal traffic from server to user B")
        self.assertEqual(ng.log, ["Normal traffic from user A to server", "Normal traffic from server to user B"])

    def test_simulated_attacks(self):
        ng = NetworkGuard()
        ng.monitor_traffic("Unauthorized access attempt by IP: 192.168.1.1")
        ng.monitor_traffic("Unusual data transfer pattern detected in server logs")
        ng.monitor_traffic("Malware signature found in incoming traffic")
        self.assertEqual(ng.log, ["Unauthorized access attempt by IP: 192.168.1.1", "Unusual data transfer pattern detected in server logs", "Malware signature found in incoming traffic"])

if __name__ == '__main__':
    unittest.main()ng.monitor_traffic("Unexpected shutdown simulation")
ng.monitor_traffic("Network disruption test")
    ng.monitor_traffic("Unusual data transfer pattern detected in server logs")
    ng.monitor_traffic("Malware signature found in incoming traffic")

    # View logsprint("Network Activities Log:")unittest.main()    ng.view_logs()
        unittest.main()unittest.main()ng.monitor_traffic("Unexpected shutdown simulation")
ng.monitor_traffic("Network disruption test")ng.view_logs()

# Run test cases
test_network_guard()