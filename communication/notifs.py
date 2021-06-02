from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS


# Initializing the flask object


def create_socket_io_app():
    app = Flask(__name__)
    CORS(app)
    CORS(app, resources={
        r"/.*": {
            "origins": "*",
            "Content-Type": "application/json"
        }
    })
    app.config['CORS_HEADERS'] = 'Content-Type'
    io = SocketIO(app, cors_allowed_origins='*')
    client_session_map = {}

    class WebsocketNotifications:
        def __init__(self):
            self.io = io
            self.app = app

        @io.on('connect')
        def connect(self):
            print("%s connected" % request.namespace)

        @io.on('enlist')
        def enlist(self, data):
            print("here")
            client_session_map[data["client_id"]] = request.sid

        @io.on('disconnect')
        def disconnect(self):
            print("%s disconnected" % request.sid)
            for user_id, sid in client_session_map.items():
                if request.sid == sid:
                    print(f"disconnecting {user_id}")
                    client_session_map.pop(user_id)
                    break

        @io.on('send_message')
        def send_message(self, msg, client_id):
            print(client_session_map)
            if client_id in client_session_map:
                emit('notification', msg, room=client_session_map[client_id])

        @io.on('send_error')
        def send_error(self, msg, client_id):
            emit('error', msg, room=client_session_map[client_id])

        @io.on('broadcast')
        def send_broadcast(self, msg):
            emit('broadcast', msg, broadcast=True)

    return WebsocketNotifications()


if __name__ == '__main__':
    print("SocketIO Server starting")
    ws_notification = create_socket_io_app()
    # io.run(app, port=5000)
    ws_notification.io.run(ws_notification.app, port=int(5001), debug=True)  # certfile="../secrets/cert.pem", keyfile="../secrets/key.pem")
