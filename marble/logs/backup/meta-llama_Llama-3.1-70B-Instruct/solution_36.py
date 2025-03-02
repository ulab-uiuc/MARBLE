# database.py
import sqlite3
from sqlite3 import Error
import bcrypt

class Database:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        # Create patient table
        patient_table = """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """
        self.conn.execute(patient_table)

        # Create medical records table
        medical_records_table = """
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                record TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            );
        """
        self.conn.execute(medical_records_table)

        # Create medication table
        medication_table = """
            CREATE TABLE IF NOT EXISTS medication (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                medication_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                schedule TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            );
        """
        self.conn.execute(medication_table)

        # Create consultation logs table
        consultation_logs_table = """
            CREATE TABLE IF NOT EXISTS consultation_logs (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                consultation_date TEXT NOT NULL,
                consultation_details TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            );
        """
        self.conn.execute(consultation_logs_table)

    def insert_patient(self, patient):
        sql = """
            INSERT INTO patients(name, email, password)
            VALUES(?,?,?)
        """
        self.conn.execute(sql, patient)
        self.conn.commit()

    def get_patient(self, email):
        sql = """
            SELECT * FROM patients
            WHERE email = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (email,))
        return cur.fetchone()

    def insert_medical_record(self, medical_record):
        sql = """
            INSERT INTO medical_records(patient_id, record)
            VALUES(?,?)
        """
        self.conn.execute(sql, medical_record)
        self.conn.commit()

    def get_medical_records(self, patient_id):
        sql = """
            SELECT * FROM medical_records
            WHERE patient_id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (patient_id,))
        return cur.fetchall()

    def insert_medication(self, medication):
        sql = """
            INSERT INTO medication(patient_id, medication_name, dosage, schedule)
            VALUES(?,?,?,?)
        """
        self.conn.execute(sql, medication)
        self.conn.commit()

    def get_medication(self, patient_id):
        sql = """
            SELECT * FROM medication
            WHERE patient_id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (patient_id,))
        return cur.fetchall()

    def insert_consultation_log(self, consultation_log):
        sql = """
            INSERT INTO consultation_logs(patient_id, consultation_date, consultation_details)
            VALUES(?,?,?)
        """
        self.conn.execute(sql, consultation_log)
        self.conn.commit()

    def get_consultation_logs(self, patient_id):
        sql = """
            SELECT * FROM consultation_logs
            WHERE patient_id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (patient_id,))
        return cur.fetchall()


# api.py
from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)

# Create a database instance
db = Database('healthconnect.db')
db.create_tables()

# API endpoint to register a patient
@app.route('/register', methods=['POST'])
def register_patient():
    patient = (request.json['name'], request.json['email'], request.json['password'])
    db.insert_patient(patient)
    return jsonify({'message': 'Patient registered successfully'}), 201

# API endpoint to login a patient
@app.route('/login', methods=['POST'])
def login_patient():email = request.json['email']
password = request.json['password']
patient = db.get_patient(email)
if patient and bcrypt.checkpw(password.encode('utf-8'), patient[3]):return jsonify({'message': 'Patient logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# API endpoint to add a medical record
@app.route('/medical_records', methods=['POST'])
def add_medical_record():
    medical_record = (request.json['patient_id'], request.json['record'])
    db.insert_medical_record(medical_record)
    return jsonify({'message': 'Medical record added successfully'}), 201

# API endpoint to get medical records
@app.route('/medical_records', methods=['GET'])
def get_medical_records():
    patient_id = request.args.get('patient_id')
    medical_records = db.get_medical_records(patient_id)
    return jsonify(medical_records), 200

# API endpoint to add medication
@app.route('/medication', methods=['POST'])
def add_medication():
    medication = (request.json['patient_id'], request.json['medication_name'], request.json['dosage'], request.json['schedule'])
    db.insert_medication(medication)
    return jsonify({'message': 'Medication added successfully'}), 201

# API endpoint to get medication
@app.route('/medication', methods=['GET'])
def get_medication():
    patient_id = request.args.get('patient_id')
    medication = db.get_medication(patient_id)
    return jsonify(medication), 200

# API endpoint to add consultation log
@app.route('/consultation_logs', methods=['POST'])
def add_consultation_log():
    consultation_log = (request.json['patient_id'], request.json['consultation_date'], request.json['consultation_details'])
    db.insert_consultation_log(consultation_log)
    return jsonify({'message': 'Consultation log added successfully'}), 201

# API endpoint to get consultation logs
@app.route('/consultation_logs', methods=['GET'])
def get_consultation_logs():
    patient_id = request.args.get('patient_id')
    consultation_logs = db.get_consultation_logs(patient_id)
    return jsonify(consultation_logs), 200

if __name__ == '__main__':
    app.run(debug=True)


# frontend.py
import tkinter as tk
from tkinter import messagebox
import requests

class HealthConnect:
    def __init__(self, root):
        self.root = root
        self.root.title('HealthConnect')

        # Create login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        # Create email and password labels and entries
        self.email_label = tk.Label(self.login_frame, text='Email:')
        self.email_label.pack()
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.pack()

        self.password_label = tk.Label(self.login_frame, text='Password:')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.pack()

        # Create login button
        self.login_button = tk.Button(self.login_frame, text='Login', command=self.login)
        self.login_button.pack()

        # Create register button
        self.register_button = tk.Button(self.login_frame, text='Register', command=self.register)
        self.register_button.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        response = requests.post('http://localhost:5000/login', json={'email': email, 'password': password})
        if response.status_code == 200:
            messagebox.showinfo('Login Successful', 'You have logged in successfully')
            self.login_frame.pack_forget()
            self.patient_dashboard()
        else:
            messagebox.showerror('Invalid Email or Password', 'Please try again')

    def register(self):
        self.login_frame.pack_forget()
        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack()

        # Create name, email, and password labels and entries
        self.name_label = tk.Label(self.register_frame, text='Name:')
        self.name_label.pack()
        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.pack()

        self.email_label = tk.Label(self.register_frame, text='Email:')
        self.email_label.pack()
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.pack()

        self.password_label = tk.Label(self.register_frame, text='Password:')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.register_frame, show='*')
        self.password_entry.pack()

        # Create register button
        self.register_button = tk.Button(self.register_frame, text='Register', command=self.register_patient)
        self.register_button.pack()

    def register_patient(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        response = requests.post('http://localhost:5000/register', json={'name': name, 'email': email, 'password': password})
        if response.status_code == 201:
            messagebox.showinfo('Registration Successful', 'You have registered successfully')
            self.register_frame.pack_forget()
            self.login_frame.pack()
        else:
            messagebox.showerror('Registration Failed', 'Please try again')

    def patient_dashboard(self):
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack()

        # Create medical records button
        self.medical_records_button = tk.Button(self.dashboard_frame, text='Medical Records', command=self.medical_records)
        self.medical_records_button.pack()

        # Create medication button
        self.medication_button = tk.Button(self.dashboard_frame, text='Medication', command=self.medication)
        self.medication_button.pack()

        # Create consultation logs button
        self.consultation_logs_button = tk.Button(self.dashboard_frame, text='Consultation Logs', command=self.consultation_logs)
        self.consultation_logs_button.pack()

    def medical_records(self):
        self.dashboard_frame.pack_forget()
        self.medical_records_frame = tk.Frame(self.root)
        self.medical_records_frame.pack()

        # Create medical record label and entry
        self.medical_record_label = tk.Label(self.medical_records_frame, text='Medical Record:')
        self.medical_record_label.pack()
        self.medical_record_entry = tk.Entry(self.medical_records_frame)
        self.medical_record_entry.pack()

        # Create add medical record button
        self.add_medical_record_button = tk.Button(self.medical_records_frame, text='Add Medical Record', command=self.add_medical_record)
        self.add_medical_record_button.pack()

        # Create get medical records button
        self.get_medical_records_button = tk.Button(self.medical_records_frame, text='Get Medical Records', command=self.get_medical_records)
        self.get_medical_records_button.pack()

    def add_medical_record(self):
        medical_record = self.medical_record_entry.get()
        response = requests.post('http://localhost:5000/medical_records', json={'patient_id': 1, 'record': medical_record})
        if response.status_code == 201:
            messagebox.showinfo('Medical Record Added', 'Medical record added successfully')
        else:
            messagebox.showerror('Medical Record Not Added', 'Please try again')

    def get_medical_records(self):
        response = requests.get('http://localhost:5000/medical_records', params={'patient_id': 1})
        if response.status_code == 200:
            messagebox.showinfo('Medical Records', response.text)
        else:
            messagebox.showerror('Medical Records Not Found', 'Please try again')

    def medication(self):
        self.dashboard_frame.pack_forget()
        self.medication_frame = tk.Frame(self.root)
        self.medication_frame.pack()

        # Create medication label and entry
        self.medication_label = tk.Label(self.medication_frame, text='Medication:')
        self.medication_label.pack()
        self.medication_entry = tk.Entry(self.medication_frame)
        self.medication_entry.pack()

        # Create add medication button
        self.add_medication_button = tk.Button(self.medication_frame, text='Add Medication', command=self.add_medication)
        self.add_medication_button.pack()

        # Create get medication button
        self.get_medication_button = tk.Button(self.medication_frame, text='Get Medication', command=self.get_medication)
        self.get_medication_button.pack()

    def add_medication(self):
        medication = self.medication_entry.get()
        response = requests.post('http://localhost:5000/medication', json={'patient_id': 1, 'medication_name': medication, 'dosage': '10mg', 'schedule': 'Daily'})
        if response.status_code == 201:
            messagebox.showinfo('Medication Added', 'Medication added successfully')
        else:
            messagebox.showerror('Medication Not Added', 'Please try again')

    def get_medication(self):
        response = requests.get('http://localhost:5000/medication', params={'patient_id': 1})
        if response.status_code == 200:
            messagebox.showinfo('Medication', response.text)
        else:
            messagebox.showerror('Medication Not Found', 'Please try again')

    def consultation_logs(self):
        self.dashboard_frame.pack_forget()
        self.consultation_logs_frame = tk.Frame(self.root)
        self.consultation_logs_frame.pack()

        # Create consultation log label and entry
        self.consultation_log_label = tk.Label(self.consultation_logs_frame, text='Consultation Log:')
        self.consultation_log_label.pack()
        self.consultation_log_entry = tk.Entry(self.consultation_logs_frame)
        self.consultation_log_entry.pack()

        # Create add consultation log button
        self.add_consultation_log_button = tk.Button(self.consultation_logs_frame, text='Add Consultation Log', command=self.add_consultation_log)
        self.add_consultation_log_button.pack()

        # Create get consultation logs button
        self.get_consultation_logs_button = tk.Button(self.consultation_logs_frame, text='Get Consultation Logs', command=self.get_consultation_logs)
        self.get_consultation_logs_button.pack()

    def add_consultation_log(self):
        consultation_log = self.consultation_log_entry.get()
        response = requests.post('http://localhost:5000/consultation_logs', json={'patient_id': 1, 'consultation_date': '2022-01-01', 'consultation_details': consultation_log})
        if response.status_code == 201:
            messagebox.showinfo('Consultation Log Added', 'Consultation log added successfully')
        else:
            messagebox.showerror('Consultation Log Not Added', 'Please try again')

    def get_consultation_logs(self):
        response = requests.get('http://localhost:5000/consultation_logs', params={'patient_id': 1})
        if response.status_code == 200:
            messagebox.showinfo('Consultation Logs', response.text)
        else:
            messagebox.showerror('Consultation Logs Not Found', 'Please try again')

if __name__ == '__main__':
    root = tk.Tk()
    app = HealthConnect(root)
    root.mainloop()