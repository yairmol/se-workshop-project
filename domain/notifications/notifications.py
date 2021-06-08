from typing import Dict


class INotifications:
    def send_message(self, user_id, msg):
        """Send the msg to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_error(self, user_id, msg):
        """Send an error message to an enlisted client with client_id"""
        raise NotImplementedError()

    def add_client(self, user_id):
        raise NotImplementedError()

    def on_sub_login(self, user_id, username):
        raise NotImplementedError()

    def disconnect(self, user_id):
        raise NotImplementedError()

    def send_broadcast(self, msg):
        """Send msg to all enlisted users"""
        raise NotImplementedError()


class Notifications(INotifications):

    __instance = None
    __comm = None

    @staticmethod
    def get_notifications():
        if not Notifications.__instance:
            Notifications.__instance = Notifications()
        return Notifications.__instance

    def __init__(self):
        self.subs_to_clients: Dict[str, int] = {}
        self.clients = []

    def add_client(self, user_id):
        self.clients.append(user_id)

    def on_sub_login(self, user_id, username):
        assert user_id in self.clients
        self.subs_to_clients[username] = user_id

    def disconnect(self, user_id):
        if user_id in self.clients:
            self.clients.remove(user_id)
        for username, other_user_id in self.subs_to_clients.items():
            if other_user_id == user_id:
                self.subs_to_clients.pop(username)
                break

    def send_message(self, user_id, msg):
        assert user_id in self.clients, "can't send message to unlisted user"
        Notifications.__comm.send_message(msg, client_id=user_id)

    def send_error(self, user_id, msg):
        assert user_id in self.clients, "can't send error message to unlisted user"
        Notifications.__comm.send_message(msg, client_id=user_id)

    def send_broadcast(self, msg):
        Notifications.__comm.send_broadcast(msg)

    @classmethod
    def set_communication(cls, comm):
        cls.__comm = comm
