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

# Database class
class Database:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        # Create user profiles table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)
        ''')

        # Create symptom logs table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS symptom_logs
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, symptom TEXT, severity INTEGER, duration INTEGER, log_date TEXT, FOREIGN KEY (user_id) REFERENCES users (id))
        ''')

        # Create medical conditions table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS medical_conditions
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, condition TEXT, diagnosis_date TEXT, FOREIGN KEY (user_id) REFERENCES users (id))
        ''')

    def insert_user(self, name, email):
        self.conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()

    def insert_symptom_log(self, user_id, symptom, severity, duration):
        self.conn.execute('INSERT INTO symptom_logs (user_id, symptom, severity, duration, log_date) VALUES (?, ?, ?, ?, ?)', (user_id, symptom, severity, duration, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def insert_medical_condition(self, user_id, condition, diagnosis_date):
        self.conn.execute('INSERT INTO medical_conditions (user_id, condition, diagnosis_date) VALUES (?, ?, ?)', (user_id, condition, diagnosis_date))
        self.conn.commit()

    def get_user_symptom_logs(self, user_id):
        cursor = self.conn.execute('SELECT * FROM symptom_logs WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    def get_user_medical_conditions(self, user_id):
        cursor = self.conn.execute('SELECT * FROM medical_conditions WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

# Recommendation Engine class
class RecommendationEngine:def make_recommendation(self, user_id, symptom_logs, medical_conditions):
    # Combine symptom logs and medical conditions into a single feature set
    combined_data = []
    for symptom_log in symptom_logs:
        combined_data.append(symptom_log[2] + ' ' + symptom_log[3] + ' ' + symptom_log[4])
    for medical_condition in medical_conditions:
        combined_data.append(medical_condition[2] + ' ' + medical_condition[3])
    # Use the combined feature set to train the machine learning model
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(combined_data)
    y = np.array([1] * len(symptom_logs) + [0] * len(medical_conditions))
    self.train_model(X, y)
    # Use the trained model to make a recommendation
    recommendation = self.model.predict(X)
    return recommendationfrom sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([symptom_log[2] for symptom_log in symptom_logs])y = np.array([symptom_log[3] for symptom_log in symptom_logs])
        self.train_model(X, y)recommendation = self.model.predict(X)
return recommendationreturn recommendation

# HealthHub class
class HealthHub:
    def __init__(self, root):
        self.root = root
        self.root.title('HealthHub')
        self.database = Database('health_hub.db')
        self.database.create_tables()
        self.recommendation_engine = RecommendationEngine()
        self.user_id = None

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.symptom_log_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.symptom_log_tab, text='Symptom Log')

        self.medical_condition_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medical_condition_tab, text='Medical Condition')

        self.recommendation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendation_tab, text='Recommendation')

        # Create symptom log tab
        self.create_symptom_log_tab()

        # Create medical condition tab
        self.create_medical_condition_tab()

        # Create recommendation tab
        self.create_recommendation_tab()

    def create_symptom_log_tab(self):
        # Create symptom log form
        self.symptom_log_form = ttk.Frame(self.symptom_log_tab)
        self.symptom_log_form.pack(pady=10)

        self.symptom_label = ttk.Label(self.symptom_log_form, text='Symptom:')
        self.symptom_label.pack()

        self.symptom_entry = ttk.Entry(self.symptom_log_form, width=50)
        self.symptom_entry.pack()

        self.severity_label = ttk.Label(self.symptom_log_form, text='Severity:')
        self.severity_label.pack()

        self.severity_entry = ttk.Entry(self.symptom_log_form, width=50)
        self.severity_entry.pack()

        self.duration_label = ttk.Label(self.symptom_log_form, text='Duration:')
        self.duration_label.pack()

        self.duration_entry = ttk.Entry(self.symptom_log_form, width=50)
        self.duration_entry.pack()

        self.log_button = ttk.Button(self.symptom_log_form, text='Log Symptom', command=self.log_symptom)
        self.log_button.pack()

        # Create symptom log listbox
        self.symptom_log_listbox = tk.Listbox(self.symptom_log_tab)
        self.symptom_log_listbox.pack(pady=10)

    def create_medical_condition_tab(self):
        # Create medical condition form
        self.medical_condition_form = ttk.Frame(self.medical_condition_tab)
        self.medical_condition_form.pack(pady=10)

        self.condition_label = ttk.Label(self.medical_condition_form, text='Condition:')
        self.condition_label.pack()

        self.condition_entry = ttk.Entry(self.medical_condition_form, width=50)
        self.condition_entry.pack()

        self.diagnosis_date_label = ttk.Label(self.medical_condition_form, text='Diagnosis Date:')
        self.diagnosis_date_label.pack()

        self.diagnosis_date_entry = ttk.Entry(self.medical_condition_form, width=50)
        self.diagnosis_date_entry.pack()

        self.add_button = ttk.Button(self.medical_condition_form, text='Add Condition', command=self.add_medical_condition)
        self.add_button.pack()

        # Create medical condition listbox
        self.medical_condition_listbox = tk.Listbox(self.medical_condition_tab)
        self.medical_condition_listbox.pack(pady=10)

    def create_recommendation_tab(self):
        # Create recommendation label
        self.recommendation_label = ttk.Label(self.recommendation_tab, text='Recommendation:')
        self.recommendation_label.pack(pady=10)

        # Create recommendation button
        self.recommendation_button = ttk.Button(self.recommendation_tab, text='Get Recommendation', command=self.get_recommendation)
        self.recommendation_button.pack()

    def log_symptom(self):
        # Get user input
        symptom = self.symptom_entry.get()
        severity = self.severity_entry.get()
        duration = self.duration_entry.get()

        # Insert symptom log into database
        self.database.insert_symptom_log(self.user_id, symptom, severity, duration)

        # Update symptom log listbox
        self.update_symptom_log_listbox()

    def add_medical_condition(self):
        # Get user input
        condition = self.condition_entry.get()
        diagnosis_date = self.diagnosis_date_entry.get()

        # Insert medical condition into database
        self.database.insert_medical_condition(self.user_id, condition, diagnosis_date)

        # Update medical condition listbox
        self.update_medical_condition_listbox()

    def update_symptom_log_listbox(self):
        # Get user's symptom logs from database
        symptom_logs = self.database.get_user_symptom_logs(self.user_id)

        # Update symptom log listbox
        self.symptom_log_listbox.delete(0, tk.END)
        for symptom_log in symptom_logs:
            self.symptom_log_listbox.insert(tk.END, f'Symptom: {symptom_log[2]}, Severity: {symptom_log[3]}, Duration: {symptom_log[4]}')

    def update_medical_condition_listbox(self):
        # Get user's medical conditions from database
        medical_conditions = self.database.get_user_medical_conditions(self.user_id)

        # Update medical condition listbox
        self.medical_condition_listbox.delete(0, tk.END)
        for medical_condition in medical_conditions:
            self.medical_condition_listbox.insert(tk.END, f'Condition: {medical_condition[2]}, Diagnosis Date: {medical_condition[3]}')

    def get_recommendation(self):
        # Get user's symptom logs and medical conditions from database
        symptom_logs = self.database.get_user_symptom_logs(self.user_id)
        medical_conditions = self.database.get_user_medical_conditions(self.user_id)

        # Use recommendation engine to make recommendation
        recommendation = self.recommendation_engine.make_recommendation(self.user_id, symptom_logs, medical_conditions)

        # Update recommendation label
        self.recommendation_label['text'] = f'Recommendation: {recommendation}'

    def run(self):
        # Create login form
        self.login_form = ttk.Frame(self.root)
        self.login_form.pack(pady=10)

        self.name_label = ttk.Label(self.login_form, text='Name:')
        self.name_label.pack()

        self.name_entry = ttk.Entry(self.login_form, width=50)
        self.name_entry.pack()

        self.email_label = ttk.Label(self.login_form, text='Email:')
        self.email_label.pack()

        self.email_entry = ttk.Entry(self.login_form, width=50)
        self.email_entry.pack()

        self.login_button = ttk.Button(self.login_form, text='Login', command=self.login)
        self.login_button.pack()

        self.root.mainloop()

    def login(self):
        # Get user input
        name = self.name_entry.get()
        email = self.email_entry.get()

        # Insert user into database
        self.database.insert_user(name, email)

        # Get user's id
        cursor = self.database.conn.execute('SELECT id FROM users WHERE name = ? AND email = ?', (name, email))
        self.user_id = cursor.fetchone()[0]

        # Destroy login form
        self.login_form.destroy()

        # Update symptom log listbox
        self.update_symptom_log_listbox()

        # Update medical condition listbox
        self.update_medical_condition_listbox()

if __name__ == '__main__':
    root = tk.Tk()
    health_hub = HealthHub(root)
    health_hub.run()