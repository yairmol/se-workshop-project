import json
import sys

from communication.api import create_app
from config.config import config, ConfigFields as cf


def main():
    """
    argv: (program_name) + [<configuration-file-path>]
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            my_config = json.load(f)
            config.update(my_config)
    app = create_app()
    cert_info = config[cf.CERTIFICATE_PATH]
    app.run(
        port=config[cf.SEVER_PORT],
        debug=True,
        ssl_context=(cert_info[cf.CERTIFICATE], cert_info[cf.KEY])
    )


if __name__ == '__main__':
    main()
