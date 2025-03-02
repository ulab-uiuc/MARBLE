# art_collab.py

import os
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectIdimport bcrypt
class UserAuth:
    def __init__(self):
        self.users_collection = MongoClient('mongodb://localhost:27017/')['art_collab']['users']def register(self, username, password):
    if self.users_collection.find_one({'username': username}):
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    self.users_collection.insert_one({'username': username, 'password': hashed_password})
    return Truedef login(self, username, password):
        user = self.users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return True
        return False
# Initialize user authentication
user_auth = UserAuth()

# Define a class for project management
class ProjectManager:
    def __init__(self):
        self.projects = {}

    def create_project(self, project_name, username):
        project_id = str(ObjectId())
        self.projects[project_id] = {'name': project_name, 'username': username, 'canvas': {}}
        projects_collection.insert_one({'_id': ObjectId(project_id), 'name': project_name, 'username': username, 'canvas': {}})
        return project_id

    def get_project(self, project_id):
        if project_id in self.projects:
            return self.projects[project_id]
        project = projects_collection.find_one({'_id': ObjectId(project_id)})
        if project:
            return project
        return None

def update_project(self, project_id, canvas):
    if project_id not in self.projects:
        project = projects_collection.find_one({'_id': ObjectId(project_id)})
        if project is None:
            raise ValueError(f"Project with id {project_id} does not exist")
        self.projects[project_id] = project
    self.projects[project_id]['canvas'] = canvas
    projects_collection.update_one({'_id': ObjectId(project_id)}, {'$set': {'canvas': canvas}})

# Define routes for user authentication
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if user_auth.register(data['username'], data['password']):
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if user_auth.login(data['username'], data['password']):
        return jsonify({'success': True})
    return jsonify({'success': False})

# Define routes for project management
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_id = project_manager.create_project(data['project_name'], data['username'])
    return jsonify({'project_id': project_id})

@app.route('/get_project', methods=['POST'])
def get_project():
    data = request.json
    project = project_manager.get_project(data['project_id'])
    if project:
        return jsonify({'project': project})
    return jsonify({'project': None})

# Define SocketIO events for real-time collaboration
@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('update_canvas')
def update_canvas(data):
    project_id = data['project_id']
    canvas = data['canvas']
    project_manager.update_project(project_id, canvas)
    emit('update_canvas', {'project_id': project_id, 'canvas': canvas}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

# react_app.py
import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import io from 'socket.io-client';

const socket = io();

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [projectName, setProjectName] = useState('');
    const [projectId, setProjectId] = useState('');
    const [canvas, setCanvas] = useState({});

    useEffect(() => {
        socket.on('update_canvas', (data) => {
            setCanvas(data.canvas);
        });
    }, []);

    const handleRegister = () => {
        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        })
        .then((response) => response.json())
        .then((data) => console.log(data));
    };

    const handleLogin = () => {
        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        })
        .then((response) => response.json())
        .then((data) => console.log(data));
    };

    const handleCreateProject = () => {
        fetch('/create_project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_name: projectName, username }),
        })
        .then((response) => response.json())
        .then((data) => setProjectId(data.project_id));
    };

    const handleUpdateCanvas = () => {
        socket.emit('update_canvas', { project_id: projectId, canvas });
    };

    return (
        <div>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button onClick={handleRegister}>Register</button>
            <button onClick={handleLogin}>Login</button>
            <input type="text" value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project Name" />
            <button onClick={handleCreateProject}>Create Project</button>
            <button onClick={handleUpdateCanvas}>Update Canvas</button>
            <canvas width="800" height="600" style={{ border: '1px solid black' }} />
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));

# index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArtCollab</title>
    <script src="https://cdn.jsdelivr.net/npm/socket.io@2/dist/socket.io.js"></script>
</head>
<body>
    <div id="root"></div>
    <script src="react_app.js"></script>
</body>
</html>