# solution.py
# Importing required libraries
import os
import csv
import json
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_uploads import UploadManager, configure_uploads
from flask_socketio import SocketIO, emit

# Creating the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_collaborator.db'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

# Initializing the database and upload manager
db = SQLAlchemy(app)
socketio = SocketIO(app)
configure_uploads(app, UploadManager())

# Defining the user roles and permissions
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

class MatchData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('match_data', lazy=True))
    file_name = db.Column(db.String(128))
    file_type = db.Column(db.String(64))
    data = db.Column(db.Text)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('reports', lazy=True))
    title = db.Column(db.String(128))
    content = db.Column(db.Text)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('notes', lazy=True))
    content = db.Column(db.Text)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    content = db.Column(db.Text)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('chat_messages', lazy=True))
    content = db.Column(db.Text)

# Defining the user roles and permissions
roles = {
    'coach': {'name': 'Coach', 'description': 'Full access to all features'},
    'analyst': {'name': 'Analyst', 'description': 'Perform data analysis and share reports'},
    'player': {'name': 'Player', 'description': 'View performance metrics and receive feedback'}
}

# Defining the user forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChatForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Defining the routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
        user.role = Role.query.filter_by(name='player').first()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        file_name = file.filename
        file_type = file.mimetype
        data = file.read()
        match_data = MatchData(user_id=current_user.id, file_name=file_name, file_type=file_type, data=data)
        db.session.add(match_data)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('upload.html', form=form)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(user_id=current_user.id, title=form.title.data, content=form.content.data)
        db.session.add(report)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('report.html', form=form)

@app.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(user_id=current_user.id, content=form.content.data)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('note.html', form=form)

@app.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, content=form.content.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('comment.html', form=form)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    if form.validate_on_submit():
        chat_message = ChatMessage(user_id=current_user.id, content=form.content.data)
        db.session.add(chat_message)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('chat.html', form=form)

# Defining the socketio routes
@socketio.on('connect')
def connect():
    emit('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    emit('disconnect', {'data': 'Disconnected'})

@socketio.on('note')
def note(data):
    note = Note(user_id=data['user_id'], content=data['content'])
    db.session.add(note)
    db.session.commit()
    emit('note', {'data': 'Note added'})

@socketio.on('comment')
def comment(data):
    comment = Comment(user_id=data['user_id'], content=data['content'])
    db.session.add(comment)
    db.session.commit()
    emit('comment', {'data': 'Comment added'})

@socketio.on('chat')
def chat(data):
    chat_message = ChatMessage(user_id=data['user_id'], content=data['content'])
    db.session.add(chat_message)
    db.session.commit()
    emit('chat', {'data': 'Chat message added'})

# Defining the test cases
def test_upload():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.post('/upload', data={'file': 'test_file.txt'})
        assert response.status_code == 200

def test_report():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.post('/report', data={'title': 'Test Report', 'content': 'Test content'})
        assert response.status_code == 200

def test_note():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.post('/note', data={'content': 'Test note'})
        assert response.status_code == 200

def test_comment():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.post('/comment', data={'content': 'Test comment'})
        assert response.status_code == 200

def test_chat():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.post('/chat', data={'content': 'Test chat message'})
        assert response.status_code == 200

# Running the application
if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)