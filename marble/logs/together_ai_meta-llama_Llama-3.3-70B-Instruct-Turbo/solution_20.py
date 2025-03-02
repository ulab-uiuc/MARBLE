# music_mashup_battle.py
import asyncio
import websockets
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music_mashup_battle.db"
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Mashup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    tracks = db.Column(db.String(120), nullable=False)
    effects = db.Column(db.String(120), nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users =room_user = db.Table('room_user', db.Column('room_id', db.Integer, db.ForeignKey('room.id')), db.Column('user_id', db.Integer, db.ForeignKey('user.id')))
    users = db.relationship('User', secondary=room_user, backref=db.backref('rooms', lazy=True))
    mashup_id = db.Column(db.Integer, db.ForeignKey("mashup.id"), nullable=False)
room_user = db.Table('room_user', db.Column('room_id', db.Integer, db.ForeignKey('room.id')), db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

# Define routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_room", methods=["POST"])
def create_room():
    room_name = request.form["room_name"]
    user_id = request.form["user_id"]
    room = Room(name=room_name, users=user_id)
    db.session.add(room)
    db.session.commit()
    return jsonify({"room_id": room.id})

@app.route("/join_room", methods=["POST"])
def join_room():
    room_id = request.form["room_id"]
    user_id = request.form["user_id"]
    room = Room.query.get(room_id)
    room.users += "," + user_id
    db.session.commit()
    return jsonify({"room_id": room_id})

@app.route("/create_mashup", methods=["POST"])
def create_mashup():
    mashup_name = request.form["mashup_name"]
    tracks = request.form["tracks"]
    effects = request.form["effects"]
    mashup = Mashup(name=mashup_name, tracks=tracks, effects=effects)
    db.session.add(mashup)
    db.session.commit()
    return jsonify({"mashup_id": mashup.id})

@app.route("/vote_mashup", methods=["POST"])
def vote_mashup():
    mashup_id = request.form["mashup_id"]
    mashup = Mashup.query.get(mashup_id)
    mashup.votes += 1
    db.session.commit()
    return jsonify({"votes": mashup.votes})

# Define socketio events
@socketio.on("connect")
def connect():
    emit("connected", {"data": "Connected to the server"})

@socketio.on("disconnect")
def disconnect():
    print("Client disconnected")

@socketio.on("create_room")
def create_room(data):
    room_name = data["room_name"]
    user_id = data["user_id"]
    room = Room(name=room_name, users=user_id)
    db.session.add(room)
    db.session.commit()
    emit("room_created", {"room_id": room.id}, broadcast=True)

@socketio.on("join_room")
def join_room(data):
    room_id = data["room_id"]
    user_id = data["user_id"]
    room = Room.query.get(room_id)
    room.users += "," + user_id
    db.session.commit()
    emit("room_joined", {"room_id": room_id}, broadcast=True)

@socketio.on("create_mashup")
def create_mashup(data):
    mashup_name = data["mashup_name"]
    tracks = data["tracks"]
    effects = data["effects"]
    mashup = Mashup(name=mashup_name, tracks=tracks, effects=effects)
    db.session.add(mashup)
    db.session.commit()
    emit("mashup_created", {"mashup_id": mashup.id}, broadcast=True)

@socketio.on("vote_mashup")
def vote_mashup(data):
    mashup_id = data["mashup_id"]
    mashup = Mashup.query.get(mashup_id)
    mashup.votes += 1
    db.session.commit()
    emit("mashup_voted", {"votes": mashup.votes}, broadcast=True)

# Define websocket handler
async def handle_websocket(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "create_room":
                room_name = data["room_name"]
                user_id = data["user_id"]
                room = Room(name=room_name, users=user_id)
                db.session.add(room)
                db.session.commit()
                await websocket.send(json.dumps({"type": "room_created", "room_id": room.id}))
            elif data["type"] == "join_room":
                room_id = data["room_id"]
                user_id = data["user_id"]
                room = Room.query.get(room_id)
                room.users += "," + user_id
                db.session.commit()
                await websocket.send(json.dumps({"type": "room_joined", "room_id": room_id}))
            elif data["type"] == "create_mashup":
                mashup_name = data["mashup_name"]
                tracks = data["tracks"]
                effects = data["effects"]
                mashup = Mashup(name=mashup_name, tracks=tracks, effects=effects)
                db.session.add(mashup)
                db.session.commit()
                await websocket.send(json.dumps({"type": "mashup_created", "mashup_id": mashup.id}))
            elif data["type"] == "vote_mashup":
                mashup_id = data["mashup_id"]
                mashup = Mashup.query.get(mashup_id)
                mashup.votes += 1
                db.session.commit()
                await websocket.send(json.dumps({"type": "mashup_voted", "votes": mashup.votes}))
        except websockets.ConnectionClosed:
            break

# Run the app
if __name__ == "__main__":
    db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000)    asyncio.get_event_loop().run_forever()