from domain.notifications.notifications import INotifications


class NotificationsMock(INotifications):
    def __init__(self):
        self.send_notif_called = False
        self.send_broadcast_called = False
        self.send_error_called = False

    def send_notif(self, client_id, msg):
        self.send_notif_called = True

    def send_error(self, client_id, error):
        self.send_error_called = True

    def send_broadcast(self, msg):
        self.send_broadcast_called = True
