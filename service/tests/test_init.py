import unittest
import copy
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.token_module.tokenizer import Tokenizer
from service.init_dict import InitDict
from service.system_service import SystemService, InitError
import init_generator as ig

init_enter_register_login = {
    "users": ["u1"],
    "actions": [
        ig.enter("u1"),
        ig.register("u1", "user1", "password"),
        ig.login("u1", "user1", "password")
    ]
}

additional_users = ["u2"]

additional_actions = [
    ig.enter("u2"),
    ig.register("u2", "user2", "password"),
    ig.login("u2", "user2", "password"),
    ig.open_shop("u1", "shop1", "the one and only shop in the entire commerce system", add_ref="s1"),
    ig.add_product_to_shop("u1", "s1", "Bamba", "Its Osem", 30, 20, ["snacks"], add_ref="p1"),
    ig.save_product_to_cart("u2", "s1", "p1", 3),
    ig.purchase_cart("u2", {}, {}, add_ref="t1"),
]


class TestInit(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SystemService(CommerceSystemFacade(Authenticator()), Tokenizer())

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

    def test_init_many_actions(self):
        init: InitDict = copy.deepcopy(init_enter_register_login)
        init["actions"].extend(additional_actions)
        init["users"].extend(additional_users)
        bindings = self.service.init(init)
        for key in [*init["users"], "s1", "p1"]:
            self.assertIn(key, bindings)
        transactions = self.service.get_personal_purchase_history(bindings["u2"])["result"]
        self.assertEqual(len(transactions), 1)

    def test_init_bad_sequence(self):
        init = {
            "users": ["u1"],
            "actions": [
                ig.register("u1", "user1", "password")
            ]
        }
        self.assertRaises(Exception, self.service.init, init)

    def test_init_bad_sequence_2(self):
        init = {
            "users": ["u1"],
            "actions": [
                ig.enter("u1"),
                ig.login("u1", "user1", "password"),
            ]
        }
        self.assertRaises(Exception, self.service.init, init)
