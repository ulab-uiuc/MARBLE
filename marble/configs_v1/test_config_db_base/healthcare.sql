-- 1. Patients table (stores patient information)
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,  -- Unique patient ID
    first_name VARCHAR(100) NOT NULL,  -- Patient's first name
    last_name VARCHAR(100) NOT NULL,  -- Patient's last name
    date_of_birth DATE NOT NULL,  -- Patient's date of birth
    gender VARCHAR(10),  -- Patient's gender
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    phone VARCHAR(20),  -- Contact number
    address VARCHAR(255),  -- Address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Registration date
);

-- 2. Doctors table (stores doctor information)
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,  -- Unique doctor ID
    first_name VARCHAR(100) NOT NULL,  -- Doctor's first name
    last_name VARCHAR(100) NOT NULL,  -- Doctor's last name
    specialty VARCHAR(100),  -- Doctor's specialty (e.g., cardiologist, dermatologist)
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    phone VARCHAR(20),  -- Contact number
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of joining
);

-- 3. Appointments table (stores patient appointments)
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,  -- Unique appointment ID
    patient_id INT REFERENCES patients(patient_id),  -- Foreign key to patients
    doctor_id INT REFERENCES doctors(doctor_id),  -- Foreign key to doctors
    appointment_date TIMESTAMP NOT NULL,  -- Date and time of the appointment
    status VARCHAR(50) DEFAULT 'scheduled',  -- Appointment status (e.g., scheduled, completed)
    reason TEXT  -- Reason for the appointment
);

-- 4. Medical Records table (stores medical records for patients)
CREATE TABLE medical_records (
    record_id SERIAL PRIMARY KEY,  -- Unique record ID
    patient_id INT REFERENCES patients(patient_id),  -- Foreign key to patients
    doctor_id INT REFERENCES doctors(doctor_id),  -- Foreign key to doctors
    record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of the medical record
    diagnosis TEXT,  -- Diagnosis made by the doctor
    treatment TEXT,  -- Treatment prescribed by the doctor
    prescriptions TEXT  -- Prescriptions provided during the visit
);

-- 5. Treatments table (stores details of treatments for patients)
CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,  -- Unique treatment ID
    patient_id INT REFERENCES patients(patient_id),  -- Foreign key to patients
    doctor_id INT REFERENCES doctors(doctor_id),  -- Foreign key to doctors
    treatment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of treatment
    treatment_type VARCHAR(100),  -- Type of treatment (e.g., surgery, medication)
    treatment_description TEXT  -- Description of the treatment
);

-- Insert sample patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, phone, address)
VALUES
('Alice', 'Johnson', '1985-04-12', 'Female', 'alice.johnson@example.com', '123-456-7890', '123 Elm St, Springfield'),
('Bob', 'Smith', '1990-08-23', 'Male', 'bob.smith@example.com', '234-567-8901', '456 Oak St, Springfield');

-- Insert sample doctors
INSERT INTO doctors (first_name, last_name, specialty, email, phone)
VALUES
('Dr. Sarah', 'Miller', 'Cardiologist', 'dr.sarah.miller@example.com', '345-678-9012'),
('Dr. James', 'Taylor', 'Dermatologist', 'dr.james.taylor@example.com', '456-789-0123');

-- Insert sample appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, reason)
VALUES
(1, 1, '2024-12-14 09:00:00', 'scheduled', 'Routine checkup'),
(2, 2, '2024-12-14 11:00:00', 'scheduled', 'Skin rash evaluation');

-- Insert sample medical records
INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment, prescriptions)
VALUES
(1, 1, 'Hypertension', 'Lifestyle changes, medication', 'Lisinopril 10mg daily'),
(2, 2, 'Eczema', 'Topical steroids, moisturizers', 'Hydrocortisone cream');

-- Insert sample treatments
INSERT INTO treatments (patient_id, doctor_id, treatment_type, treatment_description)
VALUES
(1, 1, 'Medication', 'Prescription for hypertension medication'),
(2, 2, 'Topical Treatment', 'Application of hydrocortisone cream for eczema');

-- Query to get patient details
SELECT p.patient_id, p.first_name, p.last_name, p.date_of_birth, p.gender, p.email, p.phone
FROM patients p
WHERE p.patient_id = 1;  -- Details for Alice

-- Query to get doctor details
SELECT d.doctor_id, d.first_name, d.last_name, d.specialty, d.email, d.phone
FROM doctors d
WHERE d.doctor_id = 1;  -- Details for Dr. Sarah

-- Query to get all appointments for a patient
SELECT a.appointment_id, a.appointment_date, a.status, a.reason
FROM appointments a
WHERE a.patient_id = 1;  -- Appointments for Alice

-- Query to get medical records for a patient
SELECT mr.record_id, mr.record_date, mr.diagnosis, mr.treatment, mr.prescriptions
FROM medical_records mr
WHERE mr.patient_id = 1;  -- Medical records for Alice

-- Query to get treatments for a patient
SELECT t.treatment_id, t.treatment_date, t.treatment_type, t.treatment_description
FROM treatments t
WHERE t.patient_id = 1;  -- Treatments for Alice

-- Query to get all appointments for a doctor
SELECT a.appointment_id, a.patient_id, a.appointment_date, a.status, a.reason
FROM appointments a
WHERE a.doctor_id = 1;  -- Appointments for Dr. Sarah

-- Query to get all treatments performed by a doctor
SELECT t.treatment_id, t.patient_id, t.treatment_date, t.treatment_type, t.treatment_description
FROM treatments t
WHERE t.doctor_id = 1;  -- Treatments by Dr. Sarah

-- Query to calculate the number of appointments for each doctor
SELECT d.first_name, d.last_name, COUNT(a.appointment_id) AS num_appointments
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id;
