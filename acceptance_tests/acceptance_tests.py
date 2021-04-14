from unittest import TestCase
import threading as th

from acceptance_tests.driver import Driver
from acceptance_tests.test_data import users, shops, products, permissions
from acceptance_tests.test_utils import enter_register_and_login, add_product, fill_system_with_data


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

    def test_registration_with_empty_credentials(self):
        u = {"username": "", "email": "", "password": "password24tgf"}
        self.assertFalse(self.commerce_system.register(self.session_id, **u))

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
        user = users[0].copy()
        self.assertTrue(self.commerce_system.register(self.session_id, **user))
        user["credentials"]["password"] = "pasSwordd"
        self.assertFalse(self.commerce_system.login(self.session_id, **user["credentials"]))

    def test_logout_without_login(self):
        self.assertFalse(self.commerce_system.logout(self.session_id))

    def test_guest_cant_open_shop(self):
        # try to open shop as guest
        pass

    def test_guest_cant_get_transactions(self):
        pass


class SubscribedTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])

    def tearDown(self) -> None:
        status = self.commerce_system.exit(self.session_id)
        self.assertTrue(not status)
        self.assertTrue(self.commerce_system.logout(self.session_id))

    def test_logout(self):
        # setUp and tearDown will perform the login and logout
        self.assertTrue(True)

    def test_logout_bad_session_id(self):
        self.commerce_system.logout("non_existing_session_id")

    def test_open_shop(self):
        shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])
        self.assertIsInstance(shop_id, str)
        self.assertNotEqual(shop_id, "")

    def test_open_shop_with_existing_name(self):
        pass

    def test_register_when_logged_in(self):
        self.assertFalse(self.commerce_system.register(
            **users[2]
        ))


class ShopOwnerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])

    def test_add_product_to_shop(self):
        self.assertNotEqual(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ), "")

    def test_edit_product_in_shop(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        p = products[0].copy()
        p["id"] = prod_id
        self.assertTrue(self.commerce_system.edit_product_info(
            self.session_id, self.shop_id, **p
        ))

    def test_edit_non_existing_product_in_shop(self):
        pass
        # self.assert(add_product(
        #     self.session_id, self.commerce_system, self.shop_id, products[0]
        # ), "")

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


    def test_appoint_owner_already_appointed(self):
        pass

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

    def test_unappoint_shop_owner_by_non_owner(self):
        # the user trying to unappoint the worker is not a shop owner/manager
        pass

    def test_appoint_manager_to_owner(self):
        # not sure what is the behaviour here?
        pass

    def test_get_shop_staff(self):
        pass


class ShopManagerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        self.owner_session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.owner_session_id, **shops[0])
        self.session_id = enter_register_and_login(self.commerce_system, users[1])
        self.commerce_system.appoint_shop_manager(
            self.owner_session_id, self.shop_id, users[1]["username"], permissions[0]
        )

    def test_add_product_to_shop(self):
        self.assertNotEqual(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ), "")

    def test_edit_product_in_shop(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        p = products[0].copy()
        p["product_id"] = prod_id
        self.assertTrue(self.commerce_system.edit_product_info(
            self.session_id, self.shop_id, **p
        ))

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
    USER_I = 0
    SHOP_I = 0
    PROD_I = 0

    def setUp(self) -> None:
        self.commerce_system = Driver.get_commerce_system_facade()
        (
            self.sessions_map,  # maps session ids to users info
            self.shop_id_to_shop,  # maps shop_id to shop info
            self.shop_to_session,  # maps shop_id to their initial owner session_id
            self.product_to_shop,  # maps product_id to the shop_id it belongs
            self.shop_owners,  # maps shop_id to an additional owner session
            self.shop_managers  # maps shop_id to a shop manager session
        ) = fill_system_with_data(self.commerce_system, 5, 4, 12)
        self.sessions = list(self.sessions_map.keys())
        self.shop_ids = list(self.shop_to_session.keys())
        self.shop_to_products = {shop: [p for p, s in self.product_to_shop.items() if s == shop]
                                 for shop in self.shop_ids}
        self.session_to_shops = {sess: [shop for shop, sess2 in self.shop_to_session.items() if sess == sess2]
                                       + [shop for shop, sess2 in self.shop_owners.items() if sess == sess2]
                                       + [shop for shop, sess2 in self.shop_managers.items() if sess == sess2]
                                 for sess in self.sessions}

    def test_save_product_to_cart(self):
        self.assertTrue(self.commerce_system.save_product_to_cart(
            self.sessions[self.USER_I], self.shop_ids[self.SHOP_I],
            self.shop_to_products[self.shop_ids[self.SHOP_I]][self.PROD_I]
        ))

    def test_save_non_existing_product_to_cart(self):
        pass

    def test_get_cart_info(self):
        self.test_save_product_to_cart()
        cart_info = self.commerce_system.get_cart_info(self.sessions[self.USER_I])
        shop_id = self.shop_ids[self.SHOP_I]
        assert shop_id in cart_info
        assert self.shop_to_products[shop_id][self.PROD_I] in cart_info[shop_id]["products"]

    def test_purchase_product(self):
        user_session = self.sessions[self.USER_I]
        user_shops = self.session_to_shops[user_session]
        prod = [
            p for p in self.product_to_shop.keys()
            if all(map(lambda s: p not in self.shop_to_products[s], user_shops))
        ][self.PROD_I]
        transaction_status = self.commerce_system.purchase_product(
            user_session, self.product_to_shop[prod], prod
        )
        assert transaction_status.get("status", False)

    def test_purchase_cart(self):
        user_session = self.sessions[self.USER_I]
        user_shops = self.session_to_shops[user_session]
        prods = [
            p for p in self.product_to_shop.keys()
            if all(map(lambda s: p not in self.shop_to_products[s], user_shops))
        ]
        assert all(map(lambda p: self.commerce_system.save_product_to_cart(
            user_session, self.product_to_shop[p], p
        ), prods))
        transaction_status = self.commerce_system.purchase_cart(user_session)
        assert transaction_status.get("status", False)

    def test_get_user_transactions(self):
        self.test_purchase_product()
        self.PROD_I += 1
        self.test_purchase_product()
        self.PROD_I -= 1
        user = self.sessions[self.USER_I]
        purchase_history = self.commerce_system.get_personal_purchase_history(user)
        assert len(purchase_history) == 2

    def test_get_shop_transactions(self):
        pass

    def test_shop_manager_action_without_permissions(self):
        pass

    def test_get_system_transactions(self):
        pass


class Tests(TestCase):
    def test_get_shop_info(self):
        pass

    def test_get_shop_info_bad_shop_id(self):
        pass

    def test_search_products_by_name(self):
        pass

    def test_search_products_by_filters(self):
        pass

    def test_search_products_by_name_and_filters(self):
        pass


class ParallelismTests(TestCase):
    def test_parallel_purchase_of_last_product(self):
        pass

    def test_parallel_purchase_and_delete_of_product(self):
        pass

    def test_parallel_edit_and_delete_of_product(self):
        # product should be deleted, regardless of whether it was edited or not
        pass
