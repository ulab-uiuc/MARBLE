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

# Configuring the application
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
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

# Defining the MedicalRecord model
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    medications = db.Column(db.Text, nullable=False)

    def __init__(self, patient_id, medical_history, allergies, medications):
        self.patient_id = patient_id
        self.medical_history = medical_history
        self.allergies = allergies
        self.medications = medications

# Defining the Medication model
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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

# Defining the schema for the MedicalRecord model
class MedicalRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalRecord
        load_instance = True

# Defining the schema for the Medication model
class MedicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Medication
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
# Register a new user
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role')

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username, email, password, role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Login a user
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Username does not exist'}), 400

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 400

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# Get a user's medical records
@app.route('/medical-records', methods=['GET'])
@jwt_required
def get_medical_records():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    medical_records = MedicalRecord.query.filter_by(patient_id=user.id).all()
    schema = MedicalRecordSchema(many=True)
    return jsonify(schema.dump(medical_records)), 200

# Create a new medical record
@app.route('/medical-records', methods=['POST'])
@jwt_required
def create_medical_record():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    medical_history = request.json.get('medical_history')
    allergies = request.json.get('allergies')
    medications = request.json.get('medications')

    new_medical_record = MedicalRecord(user.id, medical_history, allergies, medications)
    db.session.add(new_medical_record)
    db.session.commit()

    return jsonify({'message': 'Medical record created successfully'}), 201

# Get a user's medications
@app.route('/medications', methods=['GET'])
@jwt_required
def get_medications():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    medications = Medication.query.filter_by(patient_id=user.id).all()
    schema = MedicationSchema(many=True)
    return jsonify(schema.dump(medications)), 200

# Create a new medication
@app.route('/medications', methods=['POST'])
@jwt_required
def create_medication():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    medication_name = request.json.get('medication_name')
    dosage = request.json.get('dosage')
    frequency = request.json.get('frequency')

    new_medication = Medication(user.id, medication_name, dosage, frequency)
    db.session.add(new_medication)
    db.session.commit()

    return jsonify({'message': 'Medication created successfully'}), 201

# Get a user's consultations
@app.route('/consultations', methods=['GET'])
@jwt_required
def get_consultations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    consultations = Consultation.query.filter_by(patient_id=user.id).all()
    schema = ConsultationSchema(many=True)
    return jsonify(schema.dump(consultations)), 200

# Create a new consultation
@app.route('/consultations', methods=['POST'])
@jwt_required
def create_consultation():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    healthcare_provider_id = request.json.get('healthcare_provider_id')
    consultation_notes = request.json.get('consultation_notes')

    new_consultation = Consultation(user.id, healthcare_provider_id, consultation_notes)
    db.session.add(new_consultation)
    db.session.commit()

    return jsonify({'message': 'Consultation created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)