# network_guard.py
# This module implements the NetworkGuard security system.

import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox

# Define a logger for NetworkGuard
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkGuard:
    """
    NetworkGuard is a security system that monitors and analyzes network traffic for potential threats and unauthorized activities.
    """
    
    def __init__(self):
        # Initialize the NetworkGuard instance
        self.server_socket = None
        self.log_file = 'network_guard.log'
        self.alerts = []
        self.settings = {
            'alert_threshold': 5,  # number of suspicious activities before alerting
            'log_level': logging.INFO
        }
        self.ui = None

    def start_server(self):
        # Start the network server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        logging.info('Network server started on port 12345')

        # Create a thread to handle incoming connections
        threading.Thread(target=self.handle_connections).start()

    def handle_connections(self):
        # Handle incoming connections
        while True:
            client_socket, address = self.server_socket.accept()
            logging.info(f'Incoming connection from {address}')

            # Create a thread to handle the client connection
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def handle_client(self, client_socket, address):
        # Handle the client connection
        try:
            data = client_socket.recv(1024)
            if data:
                logging.info(f'Received data from {address}: {data.decode()}')
                self.analyze_data(data.decode())
                client_socket.send(b'OK')
            else:
                logging.info(f'No data received from {address}')
        except Exception as e:
            logging.error(f'Error handling client connection: {e}')
        finally:
            client_socket.close()

    def analyze_data(self, data):
        # Analyze the received data for potential threats
        if 'suspicious_activity' in data:
            self.alerts.append(data)
            if len(self.alerts) >= self.settings['alert_threshold']:
                self.alert()

    def alert(self):
        # Alert the administrator of potential threats
        logging.warning('Potential threats detected!')
        self.ui.show_alert()

    def start_ui(self):
        # Start the user interface
        self.ui = NetworkGuardUI(self)
        self.ui.start()

    def save_settings(self):
        # Save the current settings
        with open('settings.json', 'w') as f:
            import json
            json.dump(self.settings, f)

    def load_settings(self):
        # Load the saved settings
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            pass

class NetworkGuardUI:
    """
    The user interface for NetworkGuard.
    """
    
    def __init__(self, network_guard):
        # Initialize the user interface
        self.network_guard = network_guard
        self.root = tk.Tk()
        self.root.title('NetworkGuard')

        # Create a frame for the log
        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(fill='both', expand=True)

        # Create a frame for the settings
        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.pack(fill='x')

        # Create a label and entry for the alert threshold
        self.alert_threshold_label = tk.Label(self.settings_frame, text='Alert Threshold:')
        self.alert_threshold_label.pack(side='left')
        self.alert_threshold_entry = tk.Entry(self.settings_frame)
        self.alert_threshold_entry.insert(0, str(self.network_guard.settings['alert_threshold']))
        self.alert_threshold_entry.pack(side='left')

        # Create a label and entry for the log level
        self.log_level_label = tk.Label(self.settings_frame, text='Log Level:')
        self.log_level_label.pack(side='left')
        self.log_level_entry = tk.Entry(self.settings_frame)
        self.log_level_entry.insert(0, str(self.network_guard.settings['log_level']))
        self.log_level_entry.pack(side='left')

        # Create a button to save the settings
        self.save_settings_button = tk.Button(self.settings_frame, text='Save Settings', command=self.save_settings)
        self.save_settings_button.pack(side='left')

        # Create a button to start the network server
        self.start_server_button = tk.Button(self.settings_frame, text='Start Server', command=self.start_server)
        self.start_server_button.pack(side='left')

        # Create a button to start the user interface
        self.start_ui_button = tk.Button(self.settings_frame, text='Start UI', command=self.start_ui)
        self.start_ui_button.pack(side='left')

        # Create a text box to display the log
        self.log_text_box = tk.Text(self.log_frame)
        self.log_text_box.pack(fill='both', expand=True)

    def start(self):
        # Start the user interface
        self.root.mainloop()

    def show_alert(self):
        # Show an alert to the administrator
        messagebox.showwarning('Potential Threats Detected', 'Potential threats detected!')

    def save_settings(self):
        # Save the current settings
        self.network_guard.settings['alert_threshold'] = int(self.alert_threshold_entry.get())
        self.network_guard.settings['log_level'] = int(self.log_level_entry.get())
        self.network_guard.save_settings()

    def start_server(self):
        # Start the network server
        self.network_guard.start_server()

    def start_ui(self):
        # Start the user interface
        self.network_guard.start_ui()

    def update_log(self, message):
        # Update the log text box
        self.log_text_box.insert('end', message + '\n')
        self.log_text_box.see('end')

def main():
    # Create a NetworkGuard instance
    network_guard = NetworkGuard()

    # Load the saved settings
    network_guard.load_settings()

    # Start the network server
    network_guard.start_server()

    # Start the user interface
    network_guard.start_ui()

if __name__ == '__main__':
    main()