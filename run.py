import argparse
import json

from communication.api import create_app
from config.config import config, ConfigFields as cf, load_config


def _parse_args():
    parser = argparse.ArgumentParser(description='Commerce System')
    parser.add_argument('-c', '--config', help="configuration file path for the system")
    parser.add_argument('-i', '--init', help="initialization file for the system")

    args = parser.parse_args()
    return args


def load_init(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    """
    usage: -c <configuration-file-path> -i <initialization-file-path>
    both the configuration and initialization files are optional
    run 'python run.py -h' for help
    """

    args = _parse_args()
    if args.config:
        load_config(args.config)
    init = None
    if args.init:
        init = load_init(args.init)
    socketio, app = create_app(init)
    cert_info = config[cf.CERTIFICATE_PATH]

    # ws = threading.Thread(target=ws_notifications.websockets_server)
    # ws.start()
    # Notifications.set_communication(ws_notifications)

    socketio.run(
        app,
        port=config[cf.SEVER_PORT],
        debug=True,
        # certfile=cert_info[cf.CERTIFICATE],
        # keyfile=cert_info[cf.KEY],
        # ssl_context=(cert_info[cf.CERTIFICATE], cert_info[cf.KEY])
    )


if __name__ == '__main__':
    main()
