from communication import notifs


class INotifications:
    def send_notif(self, client_id, msg):
        """Send the msg to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_error(self, client_id, error):
        """Send an error message to an enlisted client with client_id"""
        raise NotImplementedError()

    def send_broadcast(self, msg):
        """Send msg to all enlisted users"""
        raise NotImplementedError()

    # def on_login(self, msg):


class Notifications(INotifications):
    def send_notif(self, client_id, msg):
        notifs.send_notif(client_id, msg)

    def send_error(self, client_id, error):
        notifs.send_error(client_id, error)

    def send_broadcast(self, msg):
        notifs.send_broadcast(msg)
