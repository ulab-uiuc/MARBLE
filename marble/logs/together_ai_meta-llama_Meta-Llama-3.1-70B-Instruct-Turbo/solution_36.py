# database.py
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        # Create patient table
        patient_table = """CREATE TABLE IF NOT EXISTS patients (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            email text NOT NULL,
                            password text NOT NULL
                        );"""
        self.conn.execute(patient_table)

        # Create medical records table
        medical_records_table = """CREATE TABLE IF NOT EXISTS medical_records (
                                    id integer PRIMARY KEY,
                                    patient_id integer NOT NULL,
                                    record text NOT NULL,
                                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                                );"""
        self.conn.execute(medical_records_table)

        # Create medication table
        medication_table = """CREATE TABLE IF NOT EXISTS medications (
                              id integer PRIMARY KEY,
                              patient_id integer NOT NULL,
                              medication text NOT NULL,
                              dosage text NOT NULL,
                              schedule text NOT NULL,
                              FOREIGN KEY (patient_id) REFERENCES patients (id)
                          );"""
        self.conn.execute(medication_table)

        # Create consultations table
        consultations_table = """CREATE TABLE IF NOT EXISTS consultations (
                                  id integer PRIMARY KEY,
                                  patient_id integer NOT NULL,
                                  provider_id integer NOT NULL,
                                  consultation_date text NOT NULL,
                                  FOREIGN KEY (patient_id) REFERENCES patients (id)
                              );"""
        self.conn.execute(consultations_table)

    def insert_patient(self, patient):
        sql = """INSERT INTO patients(name, email, password)
                 VALUES(?,?,?)"""
        self.conn.execute(sql, patient)
        self.conn.commit()

    def insert_medical_record(self, medical_record):
        sql = """INSERT INTO medical_records(patient_id, record)
                 VALUES(?,?)"""
        self.conn.execute(sql, medical_record)
        self.conn.commit()

    def insert_medication(self, medication):
        sql = """INSERT INTO medications(patient_id, medication, dosage, schedule)
                 VALUES(?,?,?,?)"""
        self.conn.execute(sql, medication)
        self.conn.commit()

    def insert_consultation(self, consultation):
        sql = """INSERT INTO consultations(patient_id, provider_id, consultation_date)
                 VALUES(?,?,?)"""
        self.conn.execute(sql, consultation)
        self.conn.commit()

    def get_patient(self, patient_id):
        sql = """SELECT * FROM patients WHERE id=?"""
        cursor = self.conn.execute(sql, (patient_id,))
        return cursor.fetchone()

    def get_medical_records(self, patient_id):
        sql = """SELECT * FROM medical_records WHERE patient_id=?"""
        cursor = self.conn.execute(sql, (patient_id,))
        return cursor.fetchall()

    def get_medications(self, patient_id):
        sql = """SELECT * FROM medications WHERE patient_id=?"""
        cursor = self.conn.execute(sql, (patient_id,))
        return cursor.fetchall()

    def get_consultations(self, patient_id):
        sql = """SELECT * FROM consultations WHERE patient_id=?"""
        cursor = self.conn.execute(sql, (patient_id,))
        return cursor.fetchall()


# api.py
from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)

# Create a database instance
db = Database('healthconnect.db')
db.create_tables()

@app.route('/patients', methods=['POST'])
def create_patient():
    patient = (request.json['name'], request.json['email'], request.json['password'])
    db.insert_patient(patient)
    return jsonify({'message': 'Patient created successfully'}), 201

@app.route('/patients/<int:patient_id>/medical_records', methods=['POST'])
def create_medical_record(patient_id):
    medical_record = (patient_id, request.json['record'])
    db.insert_medical_record(medical_record)
    return jsonify({'message': 'Medical record created successfully'}), 201

@app.route('/patients/<int:patient_id>/medications', methods=['POST'])
def create_medication(patient_id):
    medication = (patient_id, request.json['medication'], request.json['dosage'], request.json['schedule'])
    db.insert_medication(medication)
    return jsonify({'message': 'Medication created successfully'}), 201

@app.route('/patients/<int:patient_id>/consultations', methods=['POST'])
def create_consultation(patient_id):
    consultation = (patient_id, request.json['provider_id'], request.json['consultation_date'])
    db.insert_consultation(consultation)
    return jsonify({'message': 'Consultation created successfully'}), 201

@app.route('/patients/<int:patient_id>/medical_records', methods=['GET'])
def get_medical_records(patient_id):
    medical_records = db.get_medical_records(patient_id)
    return jsonify(medical_records)

@app.route('/patients/<int:patient_id>/medications', methods=['GET'])
def get_medications(patient_id):
    medications = db.get_medications(patient_id)
    return jsonify(medications)

@app.route('/patients/<int:patient_id>/consultations', methods=['GET'])
def get_consultations(patient_id):
    consultations = db.get_consultations(patient_id)
    return jsonify(consultations)

if __name__ == '__main__':
    app.run(debug=True)


# frontend.py
import tkinter as tk
from tkinter import ttk
import requests

class HealthConnect:
    def __init__(self, root):
        self.root = root
        self.root.title('HealthConnect')
        self.root.geometry('800x600')

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.patient_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.patient_tab, text='Patient')

        self.medical_records_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medical_records_tab, text='Medical Records')

        self.medications_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medications_tab, text='Medications')

        self.consultations_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.consultations_tab, text='Consultations')

        # Create patient tab
        self.patient_name_label = tk.Label(self.patient_tab, text='Name:')
        self.patient_name_label.pack()
        self.patient_name_entry = tk.Entry(self.patient_tab)
        self.patient_name_entry.pack()

        self.patient_email_label = tk.Label(self.patient_tab, text='Email:')
        self.patient_email_label.pack()
        self.patient_email_entry = tk.Entry(self.patient_tab)
        self.patient_email_entry.pack()

        self.patient_password_label = tk.Label(self.patient_tab, text='Password:')
        self.patient_password_label.pack()
        self.patient_password_entry = tk.Entry(self.patient_tab, show='*')
        self.patient_password_entry.pack()

        self.create_patient_button = tk.Button(self.patient_tab, text='Create Patient', command=self.create_patient)
        self.create_patient_button.pack()

        # Create medical records tab
        self.medical_record_label = tk.Label(self.medical_records_tab, text='Medical Record:')
        self.medical_record_label.pack()
        self.medical_record_entry = tk.Entry(self.medical_records_tab)
        self.medical_record_entry.pack()

        self.create_medical_record_button = tk.Button(self.medical_records_tab, text='Create Medical Record', command=self.create_medical_record)
        self.create_medical_record_button.pack()

        # Create medications tab
        self.medication_label = tk.Label(self.medications_tab, text='Medication:')
        self.medication_label.pack()
        self.medication_entry = tk.Entry(self.medications_tab)
        self.medication_entry.pack()

        self.dosage_label = tk.Label(self.medications_tab, text='Dosage:')
        self.dosage_label.pack()
        self.dosage_entry = tk.Entry(self.medications_tab)
        self.dosage_entry.pack()

        self.schedule_label = tk.Label(self.medications_tab, text='Schedule:')
        self.schedule_label.pack()
        self.schedule_entry = tk.Entry(self.medications_tab)
        self.schedule_entry.pack()

        self.create_medication_button = tk.Button(self.medications_tab, text='Create Medication', command=self.create_medication)
        self.create_medication_button.pack()

        # Create consultations tab
        self.provider_id_label = tk.Label(self.consultations_tab, text='Provider ID:')
        self.provider_id_label.pack()
        self.provider_id_entry = tk.Entry(self.consultations_tab)
        self.provider_id_entry.pack()

        self.consultation_date_label = tk.Label(self.consultations_tab, text='Consultation Date:')
        self.consultation_date_label.pack()
        self.consultation_date_entry = tk.Entry(self.consultations_tab)
        self.consultation_date_entry.pack()

        self.create_consultation_button = tk.Button(self.consultations_tab, text='Create Consultation', command=self.create_consultation)
        self.create_consultation_button.pack()

    def create_patient(self):
        patient_name = self.patient_name_entry.get()
        patient_email = self.patient_email_entry.get()
        patient_password = self.patient_password_entry.get()
        response = requests.post('http://localhost:5000/patients', json={'name': patient_name, 'email': patient_email, 'password': patient_password})
        print(response.json())

    def create_medical_record(self):
        patient_id = 1
        medical_record = self.medical_record_entry.get()
        response = requests.post(f'http://localhost:5000/patients/{patient_id}/medical_records', json={'record': medical_record})
        print(response.json())

    def create_medication(self):
        patient_id = 1
        medication = self.medication_entry.get()
        dosage = self.dosage_entry.get()
        schedule = self.schedule_entry.get()
        response = requests.post(f'http://localhost:5000/patients/{patient_id}/medications', json={'medication': medication, 'dosage': dosage, 'schedule': schedule})
        print(response.json())

    def create_consultation(self):
        patient_id = 1
        provider_id = self.provider_id_entry.get()
        consultation_date = self.consultation_date_entry.get()
        response = requests.post(f'http://localhost:5000/patients/{patient_id}/consultations', json={'provider_id': provider_id, 'consultation_date': consultation_date})
        print(response.json())

if __name__ == '__main__':
    root = tk.Tk()
    health_connect = HealthConnect(root)
    root.mainloop()