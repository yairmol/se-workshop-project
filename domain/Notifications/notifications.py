
from communication import notifs

def send_notif(client_id, msg):
    notifs.send_notif(client_id, msg)

def send_error(client_id, error):
    notifs.send_error(client_id, error)

def send_broadcast(msg):
    notifs.send_broadcast(msg)