# models.py
from enum import Enum
from typing import List, Dict

class Role(Enum):
    ADMIN = 1
    MANAGER = 2
    MEMBER = 3

class User:
    def __init__(self, id: int, name: str, role: Role):
        self.id = id
        self.name = name
        self.role = role

class Task:
    def __init__(self, id: int, title: str, description: str, status: str, assigned_to: User):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to

class Project:
    def __init__(self, id: int, title: str, tasks: List[Task]):
        self.id = id
        self.title = title
        self.tasks = tasks

# database.py
from typing import List, Dict
from models import User, Task, Project

class Database:def add_user(self, user: User):def add_task(self, task: Task):def add_project(self, project: Project):
    with self.lock:
        self.projects[project.id] = project
    with self.lock:
        self.tasks[task.id] = taskdef add_project(self, project: Project):with self.lock: self.projects[project.id] = project        with self.lock: self.projects[project.id] = project        self.projects[project.id] = project

    def get_user(self, id: int) -> User:        with self.lock: return self.users.get(id)        return self.users.get(id)

    def get_task(self, id: int) -> Task:        with self.lock: return self.tasks.get(id)        return self.tasks.get(id)

    def get_project(self, id: int) -> Project:        with self.lock: return self.projects.get(id)        return self.projects.get(id)

# backend.py
from flask import Flask, jsonify, request
from models import User, Task, Project
from database import Database

app = Flask(__name__)
db = Database()

# Create some sample data
user1 = User(1, "John Doe", Role.ADMIN)
user2 = User(2, "Jane Doe", Role.MEMBER)
task1 = Task(1, "Task 1", "Description 1", "In Progress", user1)
task2 = Task(2, "Task 2", "Description 2", "Done", user2)
project1 = Project(1, "Project 1", [task1, task2])

db.add_user(user1)
db.add_user(user2)
db.add_task(task1)
db.add_task(task2)
db.add_project(project1)

# API Endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.values())
    return jsonify([user.__dict__ for user in users])

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(db.tasks.values())
    return jsonify([task.__dict__ for task in tasks])

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = list(db.projects.values())
    return jsonify([project.__dict__ for project in projects])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = db.get_user(user_id)
    if user:
        return jsonify(user.__dict__)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    task = db.get_task(task_id)
    if task:
        return jsonify(task.__dict__)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id: int):
    project = db.get_project(project_id)
    if project:
        return jsonify(project.__dict__)
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(len(db.tasks) + 1, data['title'], data['description'], "In Progress", db.get_user(data['assigned_to']))
    db.add_task(task)
    return jsonify(task.__dict__), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])        with db.lock: task.title = data['title']        task.title = data['title']
        task.description = data['description']
        task.status = data['status']
        task.assigned_to = db.get_user(data['assigned_to'])
        return jsonify(task.__dict__)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])        with db.lock: del db.tasks[task_id]        del db.tasks[task_id]
        return jsonify({"message": "Task deleted"})
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

# frontend.py
from flask import Flask, render_template, request, jsonify
from backend import app as backend_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = backend_app.test_client().get('/tasks')
    return jsonify(response.json)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    response = backend_app.test_client().post('/tasks', json=data)
    return jsonify(response.json), response.status_code

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    response = backend_app.test_client().get(f'/tasks/{task_id}')
    return jsonify(response.json)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    data = request.json
    response = backend_app.test_client().put(f'/tasks/{task_id}', json=data)
    return jsonify(response.json), response.status_code

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    response = backend_app.test_client().delete(f'/tasks/{task_id}')
    return jsonify(response.json), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>TeamSyncPro</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.js"></script>
</head>
<body>
    <div id="app">
        <h1>TeamSyncPro</h1>
        <ul>
            <li v-for="task in tasks" :key="task.id">
                {{ task.title }} ({{ task.status }})
                <button @click="updateTask(task.id, 'Done')">Mark as Done</button>
                <button @click="deleteTask(task.id)">Delete</button>
            </li>
        </ul>
        <form @submit.prevent="createTask">
            <input type="text" v-model="newTaskTitle" placeholder="Task title">
            <input type="text" v-model="newTaskDescription" placeholder="Task description">
            <button type="submit">Create Task</button>
        </form>
    </div>
    <script>
        new Vue({
            el: '#app',
            data: {
                tasks: [],
                newTaskTitle: '',
                newTaskDescription: ''
            },
            mounted() {
                this.getTasks();
            },
            methods: {
                getTasks() {
                    fetch('/tasks')
                        .then(response => response.json())
                        .then(data => this.tasks = data);
                },
                createTask() {
                    fetch('/tasks', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ title: this.newTaskTitle, description: this.newTaskDescription })
                    })
                        .then(response => response.json())
                        .then(data => this.tasks.push(data));
                    this.newTaskTitle = '';
                    this.newTaskDescription = '';
                },
                updateTask(id, status) {
                    fetch(`/tasks/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ status })
                    })
                        .then(response => response.json())
                        .then(data => this.tasks = this.tasks.map(task => task.id === id ? data : task));
                },
                deleteTask(id) {
                    fetch(`/tasks/${id}`, { method: 'DELETE' })
                        .then(() => this.tasks = this.tasks.filter(task => task.id !== id));
                }
            }
        });
    </script>
</body>
</html>