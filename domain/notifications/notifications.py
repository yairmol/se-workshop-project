from communication import notifs


class INotifications:
    def send_notif(self, msg, client_id=-1, username=""):
        """Send the msg to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_error(self, msg, client_id=-1, username=""):
        """Send an error message to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_broadcast(self, msg):
        """Send msg to all enlisted users"""
        raise NotImplementedError()

    def enlist_sub(self, username):
        raise NotImplementedError()


class Notifications(INotifications):
    def send_notif(self, msg, client_id=-1, username=""):
        notifs.send_notif(msg, client_id, username)

    def send_error(self, msg, client_id=-1, username=""):
        notifs.send_error(msg, client_id, username)

    def send_broadcast(self, msg):
        notifs.send_broadcast(msg)
