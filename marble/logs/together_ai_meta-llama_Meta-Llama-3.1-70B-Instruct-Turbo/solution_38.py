# health_hub.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from sqlite3 import Error
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

class HealthHub:
    def __init__(self, root):
        self.root = root
        self.root.title("HealthHub")
        self.root.geometry("800x600")

        # Create database connection
        self.conn = self.create_connection()

        # Create tables
        self.create_tables()

        # Create frontend widgets
        self.create_widgets()

    def create_connection(self):
        try:
            conn = sqlite3.connect("health_hub.db")
            return conn
        except Error as e:
            print(e)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                symptom TEXT NOT NULL,
                severity INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conditions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                condition TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Create symptom logging tab
        self.symptom_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.symptom_tab, text="Symptom Logging")

        # Create symptom logging widgets
        self.symptom_label = ttk.Label(self.symptom_tab, text="Symptom:")
        self.symptom_label.pack()
        self.symptom_entry = ttk.Entry(self.symptom_tab)
        self.symptom_entry.pack()
        self.severity_label = ttk.Label(self.symptom_tab, text="Severity (1-10):")
        self.severity_label.pack()
        self.severity_entry = ttk.Entry(self.symptom_tab)
        self.severity_entry.pack()
        self.duration_label = ttk.Label(self.symptom_tab, text="Duration (minutes):")
        self.duration_label.pack()
        self.duration_entry = ttk.Entry(self.symptom_tab)
        self.duration_entry.pack()
        self.log_button = ttk.Button(self.symptom_tab, text="Log Symptom", command=self.log_symptom)
        self.log_button.pack()

        # Create condition logging tab
        self.condition_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.condition_tab, text="Condition Logging")

        # Create condition logging widgets
        self.condition_label = ttk.Label(self.condition_tab, text="Condition:")
        self.condition_label.pack()
        self.condition_entry = ttk.Entry(self.condition_tab)
        self.condition_entry.pack()
        self.log_condition_button = ttk.Button(self.condition_tab, text="Log Condition", command=self.log_condition)
        self.log_condition_button.pack()

        # Create data visualization tab
        self.visualization_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.visualization_tab, text="Data Visualization")

        # Create data visualization widgets
        self.visualization_button = ttk.Button(self.visualization_tab, text="Visualize Data", command=self.visualize_data)
        self.visualization_button.pack()

        # Create recommendation tab
        self.recommendation_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.recommendation_tab, text="Recommendations")

        # Create recommendation widgets
        self.recommendation_button = ttk.Button(self.recommendation_tab, text="Get Recommendations", command=self.get_recommendations)
        self.recommendation_button.pack()

    def log_symptom(self):
        symptom = self.symptom_entry.get()
        severity = self.severity_entry.get()
        duration = self.duration_entry.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO symptoms (user_id, symptom, severity, duration, timestamp) VALUES (1, ?, ?, ?, ?)", (symptom, severity, duration, timestamp))
        self.conn.commit()
        messagebox.showinfo("Success", "Symptom logged successfully")

    def log_condition(self):
        condition = self.condition_entry.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO conditions (user_id, condition, timestamp) VALUES (1, ?, ?)", (condition, timestamp))
        self.conn.commit()
        messagebox.showinfo("Success", "Condition logged successfully")

    def visualize_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT severity, duration FROM symptoms")
        data = cursor.fetchall()
        severities = [row[0] for row in data]
        durations = [row[1] for row in data]
        plt.plot(severities, durations)
        plt.xlabel("Severity")
        plt.ylabel("Duration")
        plt.title("Symptom Severity vs Duration")
        plt.show()

    def get_recommendations(self):
        # Train a simple linear regression model
        cursor = self.conn.cursor()
        cursor.execute("SELECT severity, duration FROM symptoms")
        data = cursor.fetchall()
        severities = [row[0] for row in data]
        durations = [row[1] for row in data]
        X = np.array(severities).reshape(-1, 1)
        y = np.array(durations)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        # Make predictions
        predictions = model.predict(X_test)
        # Print recommendations
        for i, prediction in enumerate(predictions):
            print(f"Recommendation {i+1}: If you experience a symptom with severity {X_test[i][0]}, you may experience a duration of {prediction} minutes.")

if __name__ == "__main__":
    root = tk.Tk()
    health_hub = HealthHub(root)
    root.mainloop()