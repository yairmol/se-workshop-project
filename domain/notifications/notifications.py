import communication.notifs
import domain.commerce_system.user


class INotifications:
    def send_notif(self, msg):
        """Send the msg to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_error(self, msg):
        """Send an error message to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_broadcast(self, msg):
        """Send msg to all enlisted users"""
        raise NotImplementedError()


class Notifications(INotifications):

    clients = {}

    def __init__(self, user: domain.commerce_system.user.Subscribed):
        self.pending_messages = []
        self.user = user

    def send_notif(self, msg):
        if self.user.id in self.clients.keys():
            for msg in self.pending_messages:
                communication.notifs.send_notif(msg, client_id=self.user.id)
            communication.notifs.send_notif(msg, client_id=self.user.id)
        else:
            self.pending_messages += msg

    def send_error(self, msg):
        if self.user.id in self.clients.keys():
            for msg in self.pending_messages:
                communication.notifs.send_error(msg, client_id=self.user.id)
            communication.notifs.send_error(msg, client_id=self.user.id)
        else:
            self.pending_messages += msg

    def send_broadcast(self, msg):
        communication.notifs.send_broadcast(msg)
