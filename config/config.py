import copy
import json
from typing import Union, Any, Callable, Dict


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
    NOTIFICATIONS_COMPONENT = "notifications"
    HASH_ALG = "hash_algorithm"


FACADE_VALUES = ["real", "always_true", "always_false"]
HASH_ALGORITHMS = ["sha256", "sha2", "md5", "modulo"]


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
    ConfigFields.NOTIFICATIONS_COMPONENT: {
        "name": "websockets",
        "port": 5001,
    },
    ConfigFields.HASH_ALG: "modulo"
}


base_config = copy.deepcopy(config)


def reset_config():
    config.update(base_config)


def _levenshtein_distance(s1: str, s2: str):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def _similarity(k1, k2):
    return 1 - (2 * _levenshtein_distance(k1, k2) / (len(k1) + len(k2)))


def _find_similar_key(key, proper_keys):
    most_similar_key = ""
    for proper_key in proper_keys:
        if _similarity(key, most_similar_key) < _similarity(key, proper_key):
            most_similar_key = proper_key
    return most_similar_key


class ConfigError(Exception):
    pass


validators: Dict[str, Callable[[Any], bool]] = {
    ConfigFields.HASH_ALG: lambda v: v.lower() in HASH_ALGORITHMS,
    ConfigFields.SEVER_PORT: lambda v: isinstance(v, int),
    ConfigFields.DELIVERY_FACADE: lambda v: v in FACADE_VALUES,
    ConfigFields.PAYMENT_FACADE: lambda v: v in FACADE_VALUES,
}


def validate_config(new_config: dict):
    proper_fields = [v for k, v in ConfigFields.__dict__.items() if not k.startswith('__')]
    for k in new_config.keys():
        if k not in proper_fields:
            raise ConfigError(f"non-existing key {k}. did you mean '{_find_similar_key(k, proper_fields)}'?")
        if not validators.get(k, lambda x: True)(new_config[k]):
            raise ConfigError(f"Invalid value {new_config[k]} for key {k}")


def load_config(new_config: Union[dict, str]):
    """
    updates system configuration with new_config
    :param new_config either a dictionary with the configuration or a path to a json file
    """
    if isinstance(new_config, str):
        with open(new_config, "r") as f:
            new_config = json.load(f)
    validate_config(new_config)
    config.update(new_config)
