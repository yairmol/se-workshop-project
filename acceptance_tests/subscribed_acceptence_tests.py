from unittest import TestCase

from acceptance_tests.driver import Driver
from acceptance_tests.test_data import users, shops, products, permissions
from acceptance_tests.test_utils import enter_register_and_login, add_product


class GuestTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.session_id = self.commerce_system.enter()
        self.assertIsInstance(self.session_id, str)
        self.assertNotEqual(self.session_id, "a")

    def tearDown(self) -> None:
        status = self.commerce_system.exit(self.session_id)
        self.assertTrue(not status)

    def test_enter_exit(self):
        self.assertTrue(True)

    def test_registration_simple(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0]))

    def test_registration_with_existing_email_or_username(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0]))
        user2 = users[0].copy()
        user2["username"] = "username2"
        self.assertFalse(self.commerce_system.register(self.session_id, **user2))
        user3 = users[0].copy()
        user3["email"] = "email2@gmail.com"
        self.assertFalse(self.commerce_system.register(self.session_id, **user3))

    def test_simultaneous_registration_with_same_username(self):
        results = []
        session_id2 = self.commerce_system.enter()

        def u1():
            print("here")
            results.append(self.commerce_system.register(self.session_id, **users[0]))

        def u2():
            print("here2")
            results.append(self.commerce_system.register(session_id2, **users[0]))

        t1, t2 = th.Thread(target=u1), th.Thread(target=u2)
        t1.start(), t2.start()
        t1.join(), t2.join()
        self.assertTrue(any(results))
        self.assertFalse(all(results))

    def test_login_successful(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0]))
        self.assertTrue(self.commerce_system.login(self.session_id, **users[0]["credentials"]))

    def test_login_failed(self):
        # user hasn't registered yet
        self.assertFalse(self.commerce_system.login(self.session_id, **users[0]["credentials"]))

    def test_login_failed_bad_credentials(self):
        # user hasn't registered yet
        user = users[0].copy()
        self.assertTrue(self.commerce_system.register(self.session_id, **user))
        user["credentials"]["password"] = "pasSwordd"
        self.assertFalse(self.commerce_system.login(self.session_id, **user["credentials"]))

    def test_logout_without_login(self):
        self.assertFalse(self.commerce_system.logout(self.session_id))

    def test_logout_bad_session_id(self):
        self.commerce_system.logout(self.session_id + "str")


class SubscribedTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])

    def tearDown(self) -> None:
        status = self.commerce_system.exit(self.session_id)
        self.assertTrue(not status)
        self.assertTrue(self.commerce_system.logout(self.session_id))

    def test_logout(self):
        self.assertTrue(True)

    def test_open_shop(self):
        shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])
        self.assertIsInstance(shop_id, str)
        self.assertNotEqual(shop_id, "")

    def test_register_when_logged_in(self):
        self.assertFalse(self.commerce_system.register(
            **users[2]
        ))


class ShopOwnerOperations(TestCase):
    def register(self, **kwargs):
        self.assertTrue(self.commerce_system.register(**kwargs))

    def login(self, **kwargs):
        self.assertTrue(self.commerce_system.login(**kwargs))

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])

    def test_add_product_to_shop(self):
        self.assertTrue(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ))

    def test_edit_product_in_shop(self):
        self.assertNotEqual(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ), "")

    def test_delete_product_from_shop(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.assertTrue(self.commerce_system.delete_product(
            self.session_id, self.shop_id, prod_id
        ))

    def test_delete_non_existing_product(self):
        self.assertFalse(self.commerce_system.delete_product(
            self.session_id, self.shop_id, "39r3jrn"
        ))

    def test_appoint_shop_owner(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1]["username"]
        ))

    def test_appoint_owner_by_non_owner(self):
        other_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.appoint_shop_owner(
            other_session_id, self.shop_id, users[0]["username"]
        ))

    def test_appoint_shop_manager(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1]["username"], permissions[0]
        ))

    def test_appoint_manager_by_non_owner(self):
        other_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.appoint_shop_manager(
            other_session_id, self.shop_id, users[0]["username"], permissions[0]
        ))

    def test_unappoint_shop_manager(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1]["username"], permissions[0]
        ))
        self.assertTrue(self.commerce_system.unappoint_shop_worker(
            self.session_id, self.shop_id, users[1]["username"]
        ))

    def test_unappoint_shop_manager_by_non_appointer(self):
        u1_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1]["username"], permissions[0]
        ))
        u2_session_id = enter_register_and_login(self.commerce_system, users[2])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[2]["username"]
        ))
        # check that user2 which is a shop owner is not able to unappoint user1
        # which is a shop manager appointed by user0
        self.assertTrue(self.commerce_system.unappoint_shop_worker(
            u2_session_id, self.shop_id, users[1]["username"]
        ))

    def test_get_shop_staff(self):
        pass


class PurchasesTests(TestCase):

    def test_save_product_to_cart(self):
        pass

    def test_get_cart_info(self):
        pass

    def test_purchase_product(self):
        pass

    def test_purchase_cart(self):
        pass

    def test_get_user_transactions(self):
        pass

    def test_get_shop_transactions(self):
        pass

    def test_get_system_transactions(self):
        pass
