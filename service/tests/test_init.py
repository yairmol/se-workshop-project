import unittest
import copy
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.notifications.notifications import Notifications
from domain.token_module.tokenizer import Tokenizer
from service.init_dict import InitDict
from service.system_service import SystemService, InitError


def create_enter_register_login_of_user(user_id, username, password):
    return [
        {
            "user": user_id,
            "action": "enter",
            "params": {}
        },
        {
            "user": user_id,
            "action": "register",
            "params": {
                "username": username,
                "password": password,
            }
        },
        {
            "user": user_id,
            "action": "login",
            "params": {
                "username": username,
                "password": password,
            }
        }
    ]

init_enter_register_login = {
    "users": ["u1"],
    "actions": create_enter_register_login_of_user("u1", "user1", "password")
}

additional_users = ["u2"]

additional_actions = [
    *create_enter_register_login_of_user("u2", "user2", "password"),
    {
        "action": "open_shop",
        "user": "u1",
        "params": {
            "shop_name": "shop1",
            "description": "the one and only shop in the entire commerce system"
        },
        "ref_id": "s1"
    },
    {
        "action": "add_product_to_shop",
        "user": "u1",
        "params": {
            "shop_id": {
                "ref": "s1"
            },
            "product_name": "Bamba",
            "description": "Its Osem",
            "categories": [
                "snacks"
            ],
            "price": 30,
            "quantity": 20
        },
        "ref_id": "p1"
    },
    {
        "action": "save_product_to_cart",
        "user": "u2",
        "params": {
            "shop_id": {"ref": "s1"},
            "product_id": {"ref": "p1"},
            "amount_to_buy": 3
        },
    },
    {
        "action": "purchase_cart",
        "user": "u2",
        # "params":
    }
]


class TestInit(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SystemService(CommerceSystemFacade(Authenticator(), Notifications()), Tokenizer())

    def test_init_enter_register_login(self):
        bindings = self.service.init(init_enter_register_login)
        self.assertIsNotNone(bindings["u1"])
        self.assertTrue(self.service.logout(bindings["u1"])["status"])

    def test_init_with_ref(self):
        init: InitDict = copy.deepcopy(init_enter_register_login)
        init["actions"].extend([
            {
                "action": "open_shop",
                "user": "u1",
                "params": {
                    "shop_name": "shop1",
                    "description": "the one and only shop in the entire commerce system"
                },
                "ref_id": "s1"
            },
            {
                "action": "add_product_to_shop",
                "user": "u1",
                "params": {
                    "shop_id": {
                        "ref": "s1"
                    },
                    "product_name": "Bamba",
                    "description": "Its Osem",
                    "categories": [
                        "snacks"
                    ],
                    "price": 30,
                    "quantity": 20
                },
                "ref_id": "p1"
            },
        ])
        bindings = self.service.init(init)
        self.assertIsNotNone(bindings["s1"])
        self.assertIsNotNone(bindings["p1"])
        ret = self.service.get_product_info(bindings["u1"], bindings["s1"], bindings["p1"])
        self.assertTrue(ret["status"])
        p = ret["result"]
        self.assertEqual(p["product_name"], "Bamba")

    def test_init_bad(self):
        self.assertRaises(Exception, self.service.init, {})

    def test_init_bad_no_ref(self):
        init: InitDict = copy.deepcopy(init_enter_register_login)
        init["actions"].extend([
            {
                "action": "open_shop",
                "user": "u1",
                "params": {
                    "shop_name": "shop1",
                    "description": "the one and only shop in the entire commerce system"
                },
            },
            {
                "action": "add_product_to_shop",
                "user": "u1",
                "params": {
                    "shop_id": {
                        "ref": "s1"
                    },
                    "product_name": "Bamba",
                    "description": "Its Osem",
                    "categories": [
                        "snacks"
                    ],
                    "price": 30,
                    "quantity": 20
                },
                "ref_id": "p1"
            },
        ])
        self.assertRaises(Exception, self.service.init, init)

    # def test_init_many_actions(self):
