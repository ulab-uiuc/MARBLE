# solution.py
# Importing necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime

# Creating the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initializing the database, marshmallow, bcrypt, and jwt
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Defining the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

# Defining the Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    medication_schedules = db.relationship('MedicationSchedule', backref='patient', lazy=True)
    consultations = db.relationship('Consultation', backref='patient', lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Defining the MedicalRecord model
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)

    def __init__(self, patient_id, medical_history, allergies):
        self.patient_id = patient_id
        self.medical_history = medical_history
        self.allergies = allergies

# Defining the MedicationSchedule model
class MedicationSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)

    def __init__(self, patient_id, medication_name, dosage, frequency):
        self.patient_id = patient_id
        self.medication_name = medication_name
        self.dosage = dosage
        self.frequency = frequency

# Defining the Consultation model
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    healthcare_provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    consultation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    consultation_notes = db.Column(db.Text, nullable=False)

    def __init__(self, patient_id, healthcare_provider_id, consultation_notes):
        self.patient_id = patient_id
        self.healthcare_provider_id = healthcare_provider_id
        self.consultation_notes = consultation_notes

# Defining the schema for the User model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Defining the schema for the Patient model
class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True

# Defining the schema for the MedicalRecord model
class MedicalRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalRecord
        load_instance = True

# Defining the schema for the MedicationSchedule model
class MedicationScheduleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MedicationSchedule
        load_instance = True

# Defining the schema for the Consultation model
class ConsultationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consultation
        load_instance = True

# Creating the database tables
with app.app_context():
    db.create_all()

# Defining the API endpoints
@app.route('/register', methods=['POST'])
def register():
    # Registering a new user
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')
    user = User(username, password, role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Logging in an existing user
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/patients', methods=['GET'])
@jwt_required
def get_patients():
    # Getting all patients
    patients = Patient.query.all()
    patient_schema = PatientSchema(many=True)
    return jsonify(patient_schema.dump(patients)), 200

@app.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required
def get_patient(patient_id):
    # Getting a patient by ID
    patient = Patient.query.get(patient_id)
    if patient:
        patient_schema = PatientSchema()
        return jsonify(patient_schema.dump(patient)), 200
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients/<int:patient_id>/medical-records', methods=['GET'])
@jwt_required
def get_medical_records(patient_id):
    # Getting medical records for a patient
    patient = Patient.query.get(patient_id)
    if patient:
        medical_records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
        medical_record_schema = MedicalRecordSchema(many=True)
        return jsonify(medical_record_schema.dump(medical_records)), 200
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients/<int:patient_id>/medication-schedules', methods=['GET'])
@jwt_required
def get_medication_schedules(patient_id):
    # Getting medication schedules for a patient
    patient = Patient.query.get(patient_id)
    if patient:
        medication_schedules = MedicationSchedule.query.filter_by(patient_id=patient_id).all()
        medication_schedule_schema = MedicationScheduleSchema(many=True)
        return jsonify(medication_schedule_schema.dump(medication_schedules)), 200
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients/<int:patient_id>/consultations', methods=['GET'])
@jwt_required
def get_consultations(patient_id):
    # Getting consultations for a patient
    patient = Patient.query.get(patient_id)
    if patient:
        consultations = Consultation.query.filter_by(patient_id=patient_id).all()
        consultation_schema = ConsultationSchema(many=True)
        return jsonify(consultation_schema.dump(consultations)), 200
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients/<int:patient_id>/consultations', methods=['POST'])
@jwt_required
def create_consultation(patient_id):
    # Creating a new consultation for a patient
    patient = Patient.query.get(patient_id)
    if patient:
        healthcare_provider_id = request.json.get('healthcare_provider_id')
        consultation_notes = request.json.get('consultation_notes')healthcare_provider = User.query.get(healthcare_provider_id)
if healthcare_provider:
    consultation = Consultation(patient_id, healthcare_provider_id, consultation_notes)
    db.session.add(consultation)
    db.session.commit()
    return jsonify({'message': 'Consultation created successfully'}), 201
else:
    return jsonify({'message': 'Healthcare provider not found'}), 404
        db.session.add(consultation)
        db.session.commit()
        return jsonify({'message': 'Consultation created successfully'}), 201
    return jsonify({'message': 'Patient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)