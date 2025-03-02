# network_guard.py
import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Define a logger for NetworkGuard
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkGuard:
    def __init__(self):
        # Initialize the NetworkGuard instance
        self.logger = logging.getLogger('NetworkGuard')
        self.alerts = []
        self.settings = {
            'firewall_integration': False,
            'antivirus_integration': False,
            'log_level': 'INFO'
        }
        self.window = tk.Tk()
        self.window.title('NetworkGuard')
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(pady=10, expand=True)

        # Create tabs for real-time alerts, settings, and logs
        self.alerts_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.alerts_tab, text='Real-time Alerts')
        self.notebook.add(self.settings_tab, text='Settings')
        self.notebook.add(self.logs_tab, text='Logs')

        # Create a label and text box for real-time alerts
        self.alerts_label = ttk.Label(self.alerts_tab, text='Real-time Alerts:')
        self.alerts_label.pack()
        self.alerts_text_box = tk.Text(self.alerts_tab)
        self.alerts_text_box.pack()

        # Create a label and entry for firewall integration
        self.firewall_label = ttk.Label(self.settings_tab, text='Firewall Integration:')
        self.firewall_label.pack()
        self.firewall_entry = ttk.Entry(self.settings_tab)
        self.firewall_entry.pack()

        # Create a label and entry for antivirus integration
        self.antivirus_label = ttk.Label(self.settings_tab, text='Antivirus Integration:')
        self.antivirus_label.pack()
        self.antivirus_entry = ttk.Entry(self.settings_tab)
        self.antivirus_entry.pack()

        # Create a label and entry for log level
        self.log_level_label = ttk.Label(self.settings_tab, text='Log Level:')
        self.log_level_label.pack()
        self.log_level_entry = ttk.Entry(self.settings_tab)
        self.log_level_entry.pack()

        # Create a button to save settings
        self.save_settings_button = ttk.Button(self.settings_tab, text='Save Settings', command=self.save_settings)
        self.save_settings_button.pack()

        # Create a text box for logs
        self.logs_text_box = tk.Text(self.logs_tab)
        self.logs_text_box.pack()

        # Start the network monitoring thread
        self.network_monitoring_thread = threading.Thread(target=self.monitor_network)
        self.network_monitoring_thread.daemon = True
        self.network_monitoring_thread.start()

        # Start the GUI event loop
        self.window.mainloop()

    def monitor_network(self):
        # Create a socket to listen for incoming network traffic
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 12345))
        self.socket.listen(5)

        while True:
            # Accept incoming connections
            connection, address = self.socket.accept()

            # Receive data from the connection
            data = connection.recv(1024)

            # Log the received data
            self.logger.info(f'Received data: {data}')

            # Check for suspicious activities
            if b'suspicious' in data:
                # Alert the user of suspicious activity
                self.alerts.append(f'Suspicious activity detected: {data}')
                self.update_alerts_text_box()

            # Close the connection
            connection.close()

    def update_alerts_text_box(self):
        # Clear the text box
        self.alerts_text_box.delete(1.0, tk.END)

        # Add the alerts to the text box
        for alert in self.alerts:
            self.alerts_text_box.insert(tk.END, alert + '\n')

    def save_settings(self):
        # Get the new settings from the entries
        self.settings['firewall_integration'] = self.firewall_entry.get() == 'True'
        self.settings['antivirus_integration'] = self.antivirus_entry.get() == 'True'
        self.settings['log_level'] = self.log_level_entry.get()

        # Save the new settings
        self.logger.info(f'Saved settings: {self.settings}')

    def update_logs_text_box(self):
        # Clear the text box
        self.logs_text_box.delete(1.0, tk.END)

        # Add the logs to the text box
        for log in self.logger.handlers[0].emit:
            self.logs_text_box.insert(tk.END, log + '\n')

# Create an instance of NetworkGuard
network_guard = NetworkGuard()