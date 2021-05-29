import json
import os

import eventlet
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

# Initializing the flask object
import domain.notifications.notifications

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

@io.on('connect')
def connect():
    print("%s connected" % request.namespace)

@io.on('enlist')
def enlist(data):
    domain.notifications.notifications.clients[data["client_id"]] = request.sid

@io.on('disconnect')
def disconnect():
    print("%s disconnected" % request.sid)
    clients = domain.notifications.notifications.clients
    for k in clients.keys():
        if clients[k] == request.sid:
            del clients[k]

@io.on('send_notif')
def send_notif(msg, client_id):
    emit('notification', msg, room=domain.notifications.notifications.clients[client_id])


@io.on('send_error')
def send_error(msg, client_id):
    emit('error', msg, room=domain.notifications.notifications[client_id])


@io.on('broadcast')
def send_broadcast(msg):
    emit('broadcast', msg, broadcast=True)


# If you are running it using python <filename> then below command will be used
if __name__ == '__main__':
    print("Server starting")
    # io.run(app, port=5000)
    io.run(app, port=int(5000), debug=True, certfile="../secrets/cert.pem", keyfile="../secrets/key.pem")
