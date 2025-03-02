# solution.py

# Importing necessary libraries
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Database schema
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptom_logs (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                symptom TEXT NOT NULL,
                severity REAL NOT NULL,
                duration INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def insert_user(self, name, email):
        self.cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()

    def insert_symptom_log(self, user_id, symptom, severity, duration, date):
        self.cursor.execute('INSERT INTO symptom_logs (user_id, symptom, severity, duration, date) VALUES (?, ?, ?, ?, ?)', (user_id, symptom, severity, duration, date))
        self.conn.commit()

    def get_user_symptoms(self, user_id):
        self.cursor.execute('SELECT * FROM symptom_logs WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# Recommendation Engine
class RecommendationEngine:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train_model(self, data):
        X = data[['severity', 'duration']]
        y = data['symptom']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict(self, data):
        return self.model.predict(data)

# Frontend
class Frontend:
    def __init__(self, root):
        self.root = root
        self.root.title('HealthHub')
        self.root.geometry('800x600')

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.symptom_log_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.symptom_log_tab, text='Symptom Log')

        self.recommendations_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendations_tab, text='Recommendations')

        # Create symptom log tab widgets
        self.symptom_log_label = ttk.Label(self.symptom_log_tab, text='Symptom Log:')
        self.symptom_log_label.pack(pady=10)

        self.symptom_log_tree = ttk.Treeview(self.symptom_log_tab)
        self.symptom_log_tree['columns'] = ('symptom', 'severity', 'duration', 'date')
        self.symptom_log_tree.column('#0', width=0, stretch=tk.NO)
        self.symptom_log_tree.column('symptom', anchor=tk.W, width=100)
        self.symptom_log_tree.column('severity', anchor=tk.W, width=50)
        self.symptom_log_tree.column('duration', anchor=tk.W, width=50)
        self.symptom_log_tree.column('date', anchor=tk.W, width=100)
        self.symptom_log_tree.heading('symptom', text='Symptom')
        self.symptom_log_tree.heading('severity', text='Severity')
        self.symptom_log_tree.heading('duration', text='Duration')
        self.symptom_log_tree.heading('date', text='Date')
        self.symptom_log_tree.pack(pady=10)

        self.log_symptom_button = ttk.Button(self.symptom_log_tab, text='Log Symptom', command=self.log_symptom)
        self.log_symptom_button.pack(pady=10)

        # Create recommendations tab widgets
        self.recommendations_label = ttk.Label(self.recommendations_tab, text='Recommendations:')
        self.recommendations_label.pack(pady=10)

        self.recommendations_text = tk.Text(self.recommendations_tab)
        self.recommendations_text.pack(pady=10)

        self.get_recommendations_button = ttk.Button(self.recommendations_tab, text='Get Recommendations', command=self.get_recommendations)
        self.get_recommendations_button.pack(pady=10)

    def log_symptom(self):
        # Create dialog for logging symptom
        dialog = tk.Toplevel(self.root)
        dialog.title('Log Symptom')

        symptom_label = ttk.Label(dialog, text='Symptom:')
        symptom_label.pack(pady=10)

        symptom_entry = ttk.Entry(dialog)
        symptom_entry.pack(pady=10)

        severity_label = ttk.Label(dialog, text='Severity (1-10):')
        severity_label.pack(pady=10)

        severity_entry = ttk.Entry(dialog)
        severity_entry.pack(pady=10)

        duration_label = ttk.Label(dialog, text='Duration (minutes):')
        duration_label.pack(pady=10)

        duration_entry = ttk.Entry(dialog)
        duration_entry.pack(pady=10)

        date_label = ttk.Label(dialog, text='Date (YYYY-MM-DD):')
        date_label.pack(pady=10)

        date_entry = ttk.Entry(dialog)
        date_entry.pack(pady=10)

        log_button = ttk.Button(dialog, text='Log Symptom', command=lambda: self.insert_symptom_log(int(symptom_entry.get()), int(severity_entry.get()), int(duration_entry.get()), date_entry.get()))
        log_button.pack(pady=10)

    def insert_symptom_log(self, user_id, symptom, severity, duration, date):
        db = Database('healthhub.db')
        db.insert_symptom_log(user_id, symptom, severity, duration, date)
        self.update_symptom_log_tree()

    def update_symptom_log_tree(self):
        db = Database('healthhub.db')
        symptoms = db.get_user_symptoms(1)
        self.symptom_log_tree.delete(*self.symptom_log_tree.get_children())
        for symptom in symptoms:
            self.symptom_log_tree.insert('', 'end', values=(symptom[1], symptom[2], symptom[3], symptom[4]))

    def get_recommendations(self):
        # Create dialog for getting recommendations
        dialog = tk.Toplevel(self.root)
        dialog.title('Get Recommendations')

        user_id_label = ttk.Label(dialog, text='User ID:')
        user_id_label.pack(pady=10)

        user_id_entry = ttk.Entry(dialog)
        user_id_entry.pack(pady=10)

        get_button = ttk.Button(dialog, text='Get Recommendations', command=lambda: self.get_recommendations_text(int(user_id_entry.get())))
        get_button.pack(pady=10)

    def get_recommendations_text(self, user_id):
        db = Database('healthhub.db')
        symptoms = db.get_user_symptoms(user_id)
        data = pd.DataFrame(symptoms, columns=['symptom', 'severity', 'duration', 'date'])
        engine = RecommendationEngine()
        engine.train_model(data)
        predictions = engine.predict(data)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, '\n'.join(predictions))

# Create frontend
root = tk.Tk()
frontend = Frontend(root)
root.mainloop()