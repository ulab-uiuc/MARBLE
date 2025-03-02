# solution.py
import osfrom flask import Flask, request, jsonify, send_file
from flask_bcrypt import Bcryptfrom flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_collaborator.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the login manager
login_manager = LoginManager(app)

# Initialize the socketio
socketio = SocketIO(app)

# Define the user roles
class Role:
    COACH = 'coach'
    ANALYST = 'analyst'
    PLAYER = 'player'

# Define the user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

# Define the file model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    filepath = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"File('{self.filename}', '{self.filepath}')"

# Define the report model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Report('{self.title}', '{self.content}')"

# Define the performance metric model
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"PerformanceMetric('{self.name}', '{self.value}')"

# Define the chat message model
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ChatMessage('{self.content}')"

# Load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register a new user
@app.route('/register', methods=['POST'])def register():
    form = RegistrationForm()
    if form.validate_on_submit():    if form.validate_on_submit() and form.role.data in [Role.COACH, Role.ANALYST, Role.PLAYER]:
        data = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data, 'role': form.role.data}        user = User(username=data['username'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'), role=data['role'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    return jsonify({'message': 'Invalid form data'}), 400data = request.get_json()user = User.query.filter_by(username=data['username']).first()
if user and bcrypt.check_password_hash(user.password, data['password']):if user:
        login_user(user)
        return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

# Logout a user
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), 200

# Upload a file
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_model = File(filename=filename, filepath=filepath, user_id=current_user.id)
        db.session.add(file_model)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully'}), 201

# Get all files
@app.route('/files', methods=['GET'])
@login_required
def get_files():
    files = File.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'filename': file.filename, 'filepath': file.filepath} for file in files]), 200

# Generate a report
@app.route('/report', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json()
    report = Report(title=data['title'], content=data['content'], user_id=current_user.id)
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Report generated successfully'}), 201

# Get all reports
@app.route('/reports', methods=['GET'])
@login_required
def get_reports():
    reports = Report.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'title': report.title, 'content': report.content} for report in reports]), 200

# Calculate performance metrics
@app.route('/performance', methods=['POST'])
@login_required
def calculate_performance():
    data = request.get_json()
    performance_metric = PerformanceMetric(name=data['name'], value=data['value'], user_id=current_user.id)
    db.session.add(performance_metric)
    db.session.commit()
    return jsonify({'message': 'Performance metric calculated successfully'}), 201

# Get all performance metrics
@app.route('/performance', methods=['GET'])
@login_required
def get_performance():
    performance_metrics = PerformanceMetric.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'name': metric.name, 'value': metric.value} for metric in performance_metrics]), 200

# Send a chat message
@socketio.on('send_message')
@login_required
def send_message(data):
    chat_message = ChatMessage(content=data['content'], user_id=current_user.id)
    db.session.add(chat_message)
    db.session.commit()
    emit('receive_message', {'content': data['content'], 'username': current_user.username}, broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app)

# tests.py
import unittest
from solution import app, db, User, File, Report, PerformanceMetric, ChatMessage

class TestSportsTeamCollaborator(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        with app.test_client() as client:
            response = client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            response = client.post('/login', json={'username': 'test', 'password': 'password'})
            self.assertEqual(response.status_code, 200)

    def test_upload_file(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            response = client.post('/upload', content_type='multipart/form-data', data={'file': (io.BytesIO(b'file content'), 'test.txt')})
            self.assertEqual(response.status_code, 201)

    def test_get_files(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            client.post('/upload', content_type='multipart/form-data', data={'file': (io.BytesIO(b'file content'), 'test.txt')})
            response = client.get('/files')
            self.assertEqual(response.status_code, 200)

    def test_generate_report(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            response = client.post('/report', json={'title': 'test report', 'content': 'test content'})
            self.assertEqual(response.status_code, 201)

    def test_get_reports(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            client.post('/report', json={'title': 'test report', 'content': 'test content'})
            response = client.get('/reports')
            self.assertEqual(response.status_code, 200)

    def test_calculate_performance(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            response = client.post('/performance', json={'name': 'test metric', 'value': 10.0})
            self.assertEqual(response.status_code, 201)

    def test_get_performance(self):
        with app.test_client() as client:
            client.post('/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'password', 'role': 'coach'})
            client.post('/login', json={'username': 'test', 'password': 'password'})
            client.post('/performance', json={'name': 'test metric', 'value': 10.0})
            response = client.get('/performance')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

# models.py
from solution import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    filepath = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"File('{self.filename}', '{self.filepath}')"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Report('{self.title}', '{self.content}')"

class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"PerformanceMetric('{self.name}', '{self.value}')"

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ChatMessage('{self.content}')"

# forms.py
from flask_wtf import FlaskFormclass RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])role = SelectField('Role', choices=[(Role.COACH, 'Coach'), (Role.ANALYST, 'Analyst'), (Role.PLAYER, 'Player')], validators=[DataRequired()])
    def validate_role(self, field):
        if field.data not in ['coach', 'analyst', 'player']:
            raise ValidationError('Invalid role')class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FileForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])

class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class PerformanceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])

class ChatForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])