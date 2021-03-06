const io = require('socket.io-client');

export default function startNotifications() {
  const socket = io.connect('http://localhost:5000');

  function registerNotifHandler(onNotificationReceived) {
    socket.on('notification', (msg) => {
      onNotificationReceived(msg);
    })
  }

  function registerNotifErrorHandler(handler) {
    socket.on('error', (msg) => {
      handler(msg);
    })
  }

  function registerBroadcastHandler(handler) {
    socket.on('broadcast', (msg) => {
      handler(msg);
    })
  }

  function enlist(client_id) {
    socket.emit('enlist', {client_id: client_id})
  }

  function unregisterHandler() {
    socket.off('notification')
  }

  function registerSystemEventHandler(onSystemEvent) {
    socket.on('system_event', (msg) => {
      onSystemEvent(msg);
    })
  }

  function isConnected() {
    return socket.connected;
  }

  socket.on('error', function (err) {
    console.log('received socket error:')
    console.log(err)
  })

  return {
    registerNotifHandler,
    registerNotifErrorHandler,
    registerBroadcastHandler,
    unregisterHandler,
    registerSystemEventHandler,
    enlist,
    isConnected,
  }
}
// const a = start();
// a.enlist({client_id: 1});