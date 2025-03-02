```python
# solution.py

# Importing necessary libraries
import os
import csv
import json
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import UploadManager, configure_uploads, UploadSet
from flask_socketio import SocketIO, emit
from threading import Thread
import pandas as pd
import numpy as np

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_collaborator.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Creating a user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), default='player')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Creating a form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Creating a form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Creating a form for uploading files
class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')

# Creating a user role system
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy=True)

# Creating a note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Creating a comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)

# Creating a chat model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Creating a performance metric model
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(64))
    value = db.Column(db.Float)

# Creating a report model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)

# Creating a live data stream model
class LiveDataStream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)

# Creating a video file model
class VideoFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(128))

# Creating a CSV file model
class CSVPFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(128))

# Creating a user role system
@app.before_first_request
def create_tables():
    db.create_all()

# Creating a user role system
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Creating a user login system
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

# Creating a user logout system
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Creating a user dashboard system
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Creating a user profile system
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Creating a user notes system
@app.route('/notes')
@login_required
def notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

# Creating a user comments system
@app.route('/comments')
@login_required
def comments():
    comments = Comment.query.filter_by(user_id=current_user.id).all()
    return render_template('comments.html', comments=comments)

# Creating a user chat system
@app.route('/chat')
@login_required
def chat():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return render_template('chat.html', chats=chats)

# Creating a user performance metrics system
@app.route('/performance-metrics')
@login_required
def performance_metrics():
    metrics = PerformanceMetric.query.all()
    return render_template('performance-metrics.html', metrics=metrics)

# Creating a user reports system
@app.route('/reports')
@login_required
def reports():
    reports = Report.query.all()
    return render_template('reports.html', reports=reports)

# Creating a user live data streams system
@app.route('/live-data-streams')
@login_required
def live_data_streams():
    streams = LiveDataStream.query.all()
    return render_template('live-data-streams.html', streams=streams)

# Creating a user video files system
@app.route('/video-files')
@login_required
def video_files():
    files = VideoFile.query.all()
    return render_template('video-files.html', files=files)

# Creating a user CSV files system
@app.route('/csv-files')
@login_required
def csv_files():
    files = CSVPFile.query.all()
    return render_template('csv-files.html', files=files)

# Creating a user role system
@app.route('/roles')
@login_required
def roles():
    roles = Role.query.all()
    return render_template('roles.html', roles=roles)

# Creating a user role system
@app.route('/role/<int:role_id>')
@login_required
def role(role_id):
    role = Role.query.get(role_id)
    return render_template('role.html', role=role)

# Creating a user role system
@app.route('/role/<int:role_id>/users')
@login_required
def role_users(role_id):
    role = Role.query.get(role_id)
    users = User.query.filter_by(role_id=role_id).all()
    return render_template('role-users.html', users=users)

# Creating a user role system
@app.route('/role/<int:role_id>/add-user')
@login_required
def role_add_user(role_id):
    role = Role.query.get(role_id)
    return render_template('role-add-user.html', role=role)

# Creating a user role system
@app.route('/role/<int:role_id>/add-user/<int:user_id>')
@login_required
def role_add_user_user(role_id, user_id):
    role = Role.query.get(role_id)
    user = User.query.get(user_id)
    user.role_id = role_id
    db.session.commit()
    return redirect(url_for('role_users', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/remove-user/<int:user_id>')
@login_required
def role_remove_user(role_id, user_id):
    role = Role.query.get(role_id)
    user = User.query.get(user_id)
    user.role_id = None
    db.session.commit()
    return redirect(url_for('role_users', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/edit')
@login_required
def role_edit(role_id):
    role = Role.query.get(role_id)
    return render_template('role-edit.html', role=role)

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete')
@login_required
def role_delete(role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add')
@login_required
def role_add(role_id):
    role = Role.query.get(role_id)
    return render_template('role-add.html', role=role)

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove')
@login_required
def role_remove(role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/add/<int:role_id>')
@login_required
def role_add_role(role_id, role_id):
    role = Role.query.get(role_id)
    new_role = Role(name=request.form['name'])
    db.session.add(new_role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/remove/<int:role_id>')
@login_required
def role_remove_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id>/edit/<int:role_id>')
@login_required
def role_edit_role(role_id, role_id):
    role = Role.query.get(role_id)
    role.name = request.form['name']
    db.session.commit()
    return redirect(url_for('role', role_id=role_id))

# Creating a user role system
@app.route('/role/<int:role_id>/delete/<int:role_id>')
@login_required
def role_delete_role(role_id, role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))

# Creating a user role system
@app.route('/role/<int:role_id