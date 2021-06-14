from unittest import TestCase

from config.config import load_config, ConfigFields, ConfigError


class ConfigTests(TestCase):
    def test_config_good(self):
        load_config({
            ConfigFields.SEVER_PORT: 100,
            ConfigFields.DELIVERY_FACADE: "real"
        })

    def test_config_bad_key(self):
        self.assertRaises(ConfigError, load_config, {
            "hash_alg": "sha256"
        })

    def test_config_bad_values(self):
        self.assertRaises(ConfigError, load_config, {
            ConfigFields.HASH_ALG: "sha2056"
        })

    def test_config_bad_values2(self):
        self.assertRaises(ConfigError, load_config, {
            ConfigFields.SEVER_PORT: "abc"
        })

    def test_config_bad_values3(self):
        self.assertRaises(ConfigError, load_config, {
            ConfigFields.PAYMENT_FACADE: "reall"
        })