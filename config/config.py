import json
from typing import Union


class ConfigFields:
    PAYMENT_SYSTEM_URL = "payment_system_url"
    DELIVERY_SYSTEM_URL = "delivery_system_url"
    PAYMENT_FACADE = "payment_facade"
    DELIVERY_FACADE = "delivery_facade"
    DATABASE_URL = "database_url"
    DATABASE_CREDENTIALS = "database_credentials"
    DATABASE_USERNAME = "username"
    DATABASE_PASSWORD = "password"
    ADMIN_CREDENTIALS = "admin_credentials"
    ADMIN_USERNAME = "username"
    ADMIN_PASSWORD = "password"
    CERTIFICATE_PATH = "certificate_path"
    CERTIFICATE = "cert"
    KEY = "key"
    SEVER_PORT = "port"
    WEBSOCKET_PORT = "ws_port"


config = {
    ConfigFields.PAYMENT_SYSTEM_URL: "https://cs-bgu-wsep.herokuapp.com/",
    ConfigFields.DELIVERY_SYSTEM_URL: "https://cs-bgu-wsep.herokuapp.com/",
    ConfigFields.PAYMENT_FACADE: "always_true",  # values: "real", "always_true", "always_false"
    ConfigFields.DELIVERY_FACADE: "always_true",  # values: "real", "always_true", "always_false"
    ConfigFields.DATABASE_URL: "?",
    ConfigFields.DATABASE_CREDENTIALS: {
        ConfigFields.DATABASE_USERNAME: "",
        ConfigFields.DATABASE_PASSWORD: "",
    },
    ConfigFields.ADMIN_CREDENTIALS: {
        ConfigFields.ADMIN_USERNAME: "admin_username",
        ConfigFields.ADMIN_PASSWORD: "admin_password"
    },
    ConfigFields.CERTIFICATE_PATH: {
        ConfigFields.CERTIFICATE: "secrets/cert.pem",
        ConfigFields.KEY: "secrets/key.pem"
    },
    ConfigFields.SEVER_PORT: 5000,
    ConfigFields.WEBSOCKET_PORT: 5001,
}


def load_config(new_config=Union[dict, str]):
    """
    updates system configuration with new_config
    :param new_config either a dictionary with the configuration or a path to a json file
    """
    if isinstance(new_config, str):
        with open(new_config, "r") as f:
            new_config = json.load(f)
    config.update(new_config)
