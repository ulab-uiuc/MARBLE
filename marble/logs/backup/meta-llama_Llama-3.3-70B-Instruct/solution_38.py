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

# Database class
class Database:
    def __init__(self, db_file):
        """
        Initialize the database connection.
        
        Args:
        db_file (str): The path to the SQLite database file.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print("Connected to SQLite Database")
        except Error as e:
            print(e)

    def create_table(self):
        """
        Create the user profiles, symptom logs, and medical condition tables.
        """
        create_user_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL
                                );"""
        create_symptom_table = """CREATE TABLE IF NOT EXISTS symptoms (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    symptom text NOT NULL,
                                    severity text NOT NULL,
                                    duration text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""
        create_condition_table = """CREATE TABLE IF NOT EXISTS conditions (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    condition text NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""
        try:
            self.conn.execute(create_user_table)
            self.conn.execute(create_symptom_table)
            self.conn.execute(create_condition_table)
        except Error as e:
            print(e)

    def insert_user(self, name, email):
        """
        Insert a new user into the users table.
        
        Args:
        name (str): The user's name.
        email (str): The user's email.
        """
        insert_user = """INSERT INTO users(name, email) VALUES (?, ?)"""
        try:
            self.conn.execute(insert_user, (name, email))
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_symptom(self, user_id, symptom, severity, duration):
        """
        Insert a new symptom log into the symptoms table.
        
        Args:
        user_id (int): The ID of the user who logged the symptom.
        symptom (str): The symptom logged.
        severity (str): The severity of the symptom.
        duration (str): The duration of the symptom.
        """
        insert_symptom = """INSERT INTO symptoms(user_id, symptom, severity, duration) VALUES (?, ?, ?, ?)"""
        try:
            self.conn.execute(insert_symptom, (user_id, symptom, severity, duration))
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_condition(self, user_id, condition):
        """
        Insert a new medical condition into the conditions table.
        
        Args:
        user_id (int): The ID of the user who has the condition.
        condition (str): The medical condition.
        """
        insert_condition = """INSERT INTO conditions(user_id, condition) VALUES (?, ?)"""
        try:
            self.conn.execute(insert_condition, (user_id, condition))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_user_data(self, user_id):
        """
        Retrieve a user's data from the database.
        
        Args:
        user_id (int): The ID of the user.
        
        Returns:
        dict: A dictionary containing the user's data.
        """
        get_user_data = """SELECT * FROM users WHERE id = ?"""
        try:
            cursor = self.conn.execute(get_user_data, (user_id,))
            user_data = cursor.fetchone()
            return user_data
        except Error as e:
            print(e)

    def get_symptom_data(self, user_id):
        """
        Retrieve a user's symptom logs from the database.
        
        Args:
        user_id (int): The ID of the user.
        
        Returns:
        list: A list of tuples containing the user's symptom logs.
        """
        get_symptom_data = """SELECT * FROM symptoms WHERE user_id = ?"""
        try:
            cursor = self.conn.execute(get_symptom_data, (user_id,))
            symptom_data = cursor.fetchall()
            return symptom_data
        except Error as e:
            print(e)

    def get_condition_data(self, user_id):
        """
        Retrieve a user's medical conditions from the database.
        
        Args:
        user_id (int): The ID of the user.
        
        Returns:
        list: A list of tuples containing the user's medical conditions.
        """
        get_condition_data = """SELECT * FROM conditions WHERE user_id = ?"""
        try:
            cursor = self.conn.execute(get_condition_data, (user_id,))
            condition_data = cursor.fetchall()
            return condition_data
        except Error as e:
            print(e)


# Recommendation Engine class
class RecommendationEngine:
    def __init__(self):
        """
        Initialize the recommendation engine.
        """
        self.model = RandomForestClassifier()

    def train_model(self, X, y):
        """
        Train the recommendation model using the provided data.
        
        Args:
        X (pd.DataFrame): The feature data.
        y (pd.Series): The target data.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print("Model Accuracy:", accuracy_score(y_test, y_pred))

    def make_recommendation(self, user_data):
        """
        Make a recommendation for a user based on their data.
        
        Args:
        user_data (dict): A dictionary containing the user's data.
        
        Returns:
        str: A recommendation for the user.
        """
        # This is a simple example and real-world implementation would require more complex logic
        # Preprocess user_data to match the format expected by the model
        user_data = pd.DataFrame([user_data])
        if user_data["symptom"] == "headache":
            return "Take a pain reliever and rest"
        else:
            return "Consult a doctor"


# Frontend class
class Frontend:
    def __init__(self, root):
        """
        Initialize the frontend.
        
        Args:
        root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("HealthHub")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)

        self.notebook.add(self.frame1, text="Log Symptom")
        self.notebook.add(self.frame2, text="View Data")
        self.notebook.add(self.frame3, text="Recommendation")

        self.log_symptom_frame()
        self.view_data_frame()
        self.recommendation_frame()

    def log_symptom_frame(self):
        """
        Create the log symptom frame.
        """
        tk.Label(self.frame1, text="Symptom:").pack()
        self.symptom_entry = tk.Entry(self.frame1)
        self.symptom_entry.pack()

        tk.Label(self.frame1, text="Severity:").pack()
        self.severity_entry = tk.Entry(self.frame1)
        self.severity_entry.pack()

        tk.Label(self.frame1, text="Duration:").pack()
        self.duration_entry = tk.Entry(self.frame1)
        self.duration_entry.pack()

        tk.Button(self.frame1, text="Log Symptom", command=self.log_symptom).pack()

    def view_data_frame(self):
        """
        Create the view data frame.
        """
        tk.Button(self.frame2, text="View Symptom Data", command=self.view_symptom_data).pack()
        tk.Button(self.frame2, text="View Condition Data", command=self.view_condition_data).pack()

    def recommendation_frame(self):
        """
        Create the recommendation frame.
        """
        tk.Button(self.frame3, text="Get Recommendation", command=self.get_recommendation).pack()

    def log_symptom(self):
        """
        Log a symptom.
        """
        symptom = self.symptom_entry.get()
        severity = self.severity_entry.get()
        duration = self.duration_entry.get()
        # Insert the symptom log into the database
        db.insert_symptom(1, symptom, severity, duration)

    def view_symptom_data(self):
        """
        View a user's symptom logs.
        """
        symptom_data = db.get_symptom_data(1)
        print(symptom_data)

    def view_condition_data(self):
        """
        View a user's medical conditions.
        """
        condition_data = db.get_condition_data(1)
        print(condition_data)

    def get_recommendation(self):
        """
        Get a recommendation for a user.
        """
        user_data = db.get_user_data(1)
        recommendation = recommendation_engine.make_recommendation(user_data)
        print(recommendation)


# Main function
def main():
    global db
    global recommendation_engine
    db = Database("healthhub.db")
    db.create_table()
    db.insert_user("John Doe", "john@example.com")
    db.insert_symptom(1, "headache", "mild", "1 day")
    db.insert_condition(1, "diabetes")

    recommendation_engine = RecommendationEngine()
    # Train the recommendation model
    # recommendation_engine.train_model(X, y)

    root = tk.Tk()
    frontend = Frontend(root)
    root.mainloop()


if __name__ == "__main__":
    main()