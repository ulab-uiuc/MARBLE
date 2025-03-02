# solution.py
# Import necessary libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Database class to handle database operations
class Database:def __init__(self, db_file):
    self.conn = None
    try:
        self.conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)def get_user_id(self, username):
        # Retrieve user ID from the database based on the username
        sql = '''SELECT id FROM user_profiles WHERE name = ?'''
        try:
            c = self.conn.cursor()
            c.execute(sql, (username,))
            row = c.fetchone()
            return row[0]
        except Error as e:
            print(e)
        # Initialize the database connection
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self):
        # Create table for user profiles
        create_table_sql = """CREATE TABLE IF NOT EXISTS user_profiles (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL
                                );"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

        # Create table for symptom logs
        create_table_sql = """CREATE TABLE IF NOT EXISTS symptom_logs (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    symptom text NOT NULL,
                                    severity text NOT NULL,
                                    duration text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES user_profiles (id)
                                );"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

        # Create table for medical conditions
        create_table_sql = """CREATE TABLE IF NOT EXISTS medical_conditions (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    condition text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES user_profiles (id)
                                );"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_data(self, table, data):
        # Insert data into the specified table
        if table == "user_profiles":
            sql = '''INSERT INTO user_profiles(name, email)
                     VALUES(?,?)'''
        elif table == "symptom_logs":
            sql = '''INSERT INTO symptom_logs(user_id, symptom, severity, duration)
                     VALUES(?,?,?,?)'''
        elif table == "medical_conditions":
            sql = '''INSERT INTO medical_conditions(user_id, condition)
                     VALUES(?,?)'''
        try:
            c = self.conn.cursor()
            c.execute(sql, data)
            self.conn.commit()
            return c.lastrowid
        except Error as e:
            print(e)

    def retrieve_data(self, table):
        # Retrieve data from the specified table
        if table == "user_profiles":
            sql = '''SELECT * FROM user_profiles'''
        elif table == "symptom_logs":
            sql = '''SELECT * FROM symptom_logs'''
        elif table == "medical_conditions":
            sql = '''SELECT * FROM medical_conditions'''
        try:
            c = self.conn.cursor()
            c.execute(sql)
            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)

# Recommendation Engine class to handle recommendation logic
class RecommendationEngine:
    def __init__(self):
        # Initialize the recommendation engine
        self.model = RandomForestClassifier()

    def train_model(self, data):
        # Train the recommendation model using the provided data
        X = data.drop(['condition'], axis=1)
        y = data['condition']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print("Model Accuracy:", accuracy_score(y_test, y_pred))

    def generate_recommendations(self, user_data):
        # Generate personalized recommendations for the user
        # This is a simplified example and actual implementation may vary based on the complexity of the model
        predictions = self.model.predict(user_data)
        return predictions

# Frontend class to handle user interface
class Frontend:
    def __init__(self, root):
def __init__(self, root, user_id):
def authenticate_user(self, username, password):
        # Authenticate the user based on the username and password
        db = Database("healthhub.db")
        # Retrieve user ID from the database
        user_id = db.get_user_id(username)
        # Verify the password
        # ... (password verification logic)
        return user_id
        self.user_id = user_id
        # Initialize the frontend
        self.root = root
        self.root.title("HealthHub")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Create frames for different tabs
        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Log Symptoms")
        self.notebook.add(self.frame2, text="View Health Data")
        self.notebook.add(self.frame3, text="Recommendations")

        # Create widgets for logging symptoms
        self.symptom_label = tk.Label(self.frame1, text="Symptom:")
        self.symptom_label.pack()
        self.symptom_entry = tk.Entry(self.frame1)
        self.symptom_entry.pack()
        self.severity_label = tk.Label(self.frame1, text="Severity:")
        self.severity_label.pack()
        self.severity_entry = tk.Entry(self.frame1)
        self.severity_entry.pack()
        self.duration_label = tk.Label(self.frame1, text="Duration:")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.frame1)
        self.duration_entry.pack()
        self.log_button = tk.Button(self.frame1, text="Log Symptoms", command=self.log_symptoms)
        self.log_button.pack()

        # Create widgets for viewing health data
        self.health_data_label = tk.Label(self.frame2, text="Health Data:")
        self.health_data_label.pack()
        self.health_data_text = tk.Text(self.frame2)
        self.health_data_text.pack()

        # Create widgets for viewing recommendations
        self.recommendations_label = tk.Label(self.frame3, text="Recommendations:")
        self.recommendations_label.pack()
        self.recommendations_text = tk.Text(self.frame3)
        self.recommendations_text.pack()

    def log_symptoms(self):
        # Log symptoms and store in the database
        symptom = self.symptom_entry.get()
        severity = self.severity_entry.get()
        duration = self.duration_entry.get()
        # Insert data into the database
        db = Database("healthhub.db")
        db.create_table()
        db.insert_data("symptom_logs", (1, symptom, severity, duration))

    def view_health_data(self):
        # Retrieve health data from the database and display in the frontend
        db = Database("healthhub.db")
        data = db.retrieve_data("symptom_logs")
        self.health_data_text.delete(1.0, tk.END)
        for row in data:
            self.health_data_text.insert(tk.END, str(row) + "\n")

    def view_recommendations(self):
        # Generate recommendations using the recommendation engine and display in the frontend
        engine = RecommendationEngine()
        # Train the model using sample data
        data = pd.DataFrame({
            'symptom': ['headache', 'fever', 'cough'],
            'severity': ['mild', 'moderate', 'severe'],
            'duration': ['1 day', '2 days', '3 days'],
            'condition': ['common cold', 'flu', 'pneumonia']
        })
        engine.train_model(data)
        # Generate recommendations for the user
        user_data = pd.DataFrame({
            'symptom': ['headache'],
            'severity': ['mild'],
            'duration': ['1 day']
        })
        recommendations = engine.generate_recommendations(user_data)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, str(recommendations))

# Create the frontendfrontend = Frontend(root, user_id)# Start the frontend
root.mainloop()