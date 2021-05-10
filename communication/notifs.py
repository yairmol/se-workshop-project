import json
import os

from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

# Initializing the flask object
app = Flask(__name__)
# by default runs on port 5000
#  Initializing the flask-websocketio

CORS(app)

CORS(app, resources={
    r"/.*": {
        "origins": "*",
        "Content-Type": "application/json"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'
io = SocketIO(app, cors_allowed_origins='*')

# app.config['SECRET_KEY'] = '../secrets/cert.pem'
# app.config['SECRET_CERT'] = '../secrets/cert.pem'

clients = {}
subscribed_clients = {}

@io.on('connect')
def connect():
    print("%s connected" % request.namespace)


@io.on('enlist')
def enlist(data):
    print("client id %s enlisting " % data["client_id"])
    print("%s sid" % request.sid)
    clients[data["client_id"]] = request.sid
    if data["username"] not in list(subscribed_clients.keys()):
        subscribed_clients[data["username"]] = {"client_id": data["client_id"], "msgs": []}
    elif data["username"]:
        subscribed_clients[data["username"]].client_id = data["client_id"]
        for msg in subscribed_clients["msgs"]:
            send_notif(data["client_id"], msg)

def enlist_sub(username):
    if username not in list(subscribed_clients.keys()):
        subscribed_clients[username] = {"client_id": -1, "msgs": []}

@io.on('disconnect')
def disconnect():
    print("%s disconnected" % request.sid)
    for k in clients.copy():
        if clients[k] == request.sid:
            del clients[k]


@io.on('send_notif')
def send_notif(msg, client_id, username=""):
    print(clients)
    if client_id in list(clients.keys()):
        emit('notification', msg, room=clients[client_id])
    elif username in subscribed_clients and username != "":
        subscribed_clients[username]["msgs"] += msg
    elif username != "":
        subscribed_clients[username] = {"client_id": client_id, "msgs": []}
    else:
        print("Guest is not enlisted")


@io.on('send_error')
def send_error(msg, client_id, username):
    if client_id in list(clients.keys()):
        emit('error', msg, room=clients[client_id])
    elif username in subscribed_clients.keys() and username != "":
        subscribed_clients[username]["msgs"] += msg
    elif username != "":
        subscribed_clients[username] = {"client_id": client_id, "msgs": []}
    else:
        print("Guest is not enlisted")


@io.on('broadcast')
def send_broadcast(msg):
    emit('broadcast', msg, broadcast=True)


# If you are running it using python <filename> then below command will be used
if __name__ == '__main__':
    print("Server starting")
    io.run(app)