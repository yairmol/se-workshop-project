import unittest
from unittest import TestCase
import threading as th

from acceptance_tests.driver import Driver
from acceptance_tests.test_data import users, shops, products, permissions
from acceptance_tests.test_utils import (
    enter_register_and_login, add_product, make_purchases, register_login_users,
    open_shops, add_products, appoint_owners_and_managers, shop_to_products,
    sessions_to_shops, get_shop_not_owned_by_user
)


class GuestTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.session_id = self.commerce_system.enter()
        self.assertIsInstance(self.session_id, str)
        self.assertNotEqual(self.session_id, "")

    def tearDown(self) -> None:
        status = self.commerce_system.exit(self.session_id)
        self.assertTrue(status)

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
        self.assertFalse(self.commerce_system.open_shop(self.session_id, **shops[0]) == "")

    def test_guest_cant_get_transactions(self):
        assert not self.commerce_system.get_personal_purchase_history(self.session_id)


class SubscribedTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
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
        self.assertTrue(self.commerce_system.open_shop(self.session_id, **shops[0]))
        self.assertFalse(self.commerce_system.open_shop(self.session_id, **shops[0]))

    def test_register_when_logged_in(self):
        self.assertFalse(self.commerce_system.register(
            **users[2]
        ))


class ShopOwnerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
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
        p["product_id"] = prod_id
        self.assertTrue(self.commerce_system.edit_product_info(
            self.session_id, self.shop_id, **p
        ))

    def test_edit_non_existing_product_in_shop(self):
        self.assertNotEqual(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ), "")
        p = products[0].copy()
        p["product_id"] = "some_non_existing_id"
        self.assertTrue(self.commerce_system.edit_product_info(
            self.session_id, self.shop_id, **p
        ), "p")

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
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1]["username"]
        ))
        self.assertFalse(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1]["username"]
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
        enter_register_and_login(self.commerce_system, users[1])
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
        u_session_id = enter_register_and_login(self.commerce_system, users[1])
        enter_register_and_login(self.commerce_system, users[2])
        self.assertFalse(self.commerce_system.unappoint_shop_worker(
            u_session_id, self.shop_id, users[2]["username"]
        ))

    def test_appoint_manager_to_owner(self):
        # not sure what is the behaviour here?
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1]["username"], permissions[0]
        ))
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1]["username"]
        ))

    def test_get_shop_staff(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1]["username"], permissions[0]
        ))
        enter_register_and_login(self.commerce_system, users[2])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1]["username"]
        ))
        shop_staff = self.commerce_system.get_shop_staff_info(self.session_id, self.shop_id)
        expected_usernames = {u["username"] for u in users[:2]}
        usernames_got = {u["username"] for u in shop_staff}
        self.assertEquals(expected_usernames, usernames_got)

    def test_get_shop_staff_by_non_owner(self):
        non_owner = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.get_shop_staff_info(non_owner, self.shop_id))


class ShopManagerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.owner_session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.owner_session_id, **shops[0])
        self.session_id = enter_register_and_login(self.commerce_system, users[1])
        self.username = users[1]["username"]
        self.commerce_system.appoint_shop_manager(
            self.owner_session_id, self.shop_id, users[1]["username"], permissions[0]
        )
        self.permissions_to_functions_map = {
            "add_product": self.commerce_system.add_product_to_shop,
            "edit_product": self.commerce_system.edit_product_info,
            "delete_product": self.commerce_system.delete_product,
        }

    def edit_manager_permissions(self, m_permissions):
        self.assertTrue(self.commerce_system.edit_manager_permissions(
            self.owner_session_id, self.shop_id, self.username, m_permissions
        ))

    def test_add_product_to_shop(self):
        self.assertNotEqual(add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        ), "")

    def test_add_product_to_shop_no_permissions(self):
        self.edit_manager_permissions([])
        self.assertFalse(add_product(
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

    def test_edit_product_in_shop_no_permission(self):
        prod_id = add_product(
            self.owner_session_id, self.commerce_system, self.shop_id, products[0]
        )
        p = products[0].copy()
        p["product_id"] = prod_id
        self.edit_manager_permissions([])
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

    def test_delete_product_from_shop_no_permission(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.edit_manager_permissions([])
        self.assertTrue(self.commerce_system.delete_product(
            self.session_id, self.shop_id, prod_id
        ))


class PurchasesTests(TestCase):
    NUM_USERS = len(users)
    NUM_SHOPS = len(shops)
    NUM_PRODUCTS = len(products)
    U1 = 0

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.sessions_to_users = register_login_users(self.commerce_system, self.NUM_USERS)
        self.sessions = list(self.sessions_to_users.keys())
        self.shop_id_to_shop, self.shop_to_opener = open_shops(self.commerce_system, self.sessions, self.NUM_SHOPS)
        self.shop_ids = list(self.shop_id_to_shop.keys())
        self.product_to_shop = add_products(self.commerce_system, self.sessions, self.shop_ids, self.NUM_PRODUCTS)
        self.shop_to_owners, self.shop_to_managers = appoint_owners_and_managers(
            self.commerce_system, self.sessions, self.sessions_to_users, self.shop_ids
        )
        self.shops_to_products = shop_to_products(self.product_to_shop, self.shop_ids)
        self.shop_to_staff, self.session_to_shops = sessions_to_shops(
            self.shop_to_opener, self.shop_to_owners, self.shops_to_products, self.sessions
        )

    def test_save_product_to_cart(self):
        user_session = self.sessions[self.U1]
        shop_id = get_shop_not_owned_by_user(user_session, self.shop_ids, self.shop_to_staff)
        product_id = self.shops_to_products[shop_id][0]
        self.assertTrue(self.commerce_system.save_product_to_cart(user_session, shop_id, product_id))

    def test_save_non_existing_product_to_cart(self):
        user = self.sessions[self.U1]
        shop_id = get_shop_not_owned_by_user(user, self.shop_ids, self.shop_to_staff)
        self.assertFalse(self.commerce_system.save_product_to_cart(
            self.sessions[self.U1], shop_id, "some_non_existing_product_id"
        ))

    def test_get_cart_info(self):
        self.test_save_product_to_cart()
        cart_info = self.commerce_system.get_cart_info(self.sessions[self.U1])
        shop_id = self.shop_ids[self.SHOP_I]
        self.assertTrue(shop_id in cart_info)
        self.assertTrue(self.shop_to_products[shop_id][self.PROD_I] in cart_info[shop_id]["products"])

    def test_purchase_product(self):
        user_session = self.sessions[self.U1]
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
        user_session = self.sessions[self.U1]
        user_shops = self.session_to_shops[user_session]
        prods = [
            p for p in self.product_to_shop.keys()
            if all(map(lambda s: p not in self.shop_to_products[s], user_shops))
        ]
        self.assertTrue(all(map(lambda p: self.commerce_system.save_product_to_cart(
            user_session, self.product_to_shop[p], p
        ), prods)))
        transaction_status = self.commerce_system.purchase_cart(user_session)
        self.assertTrue(transaction_status.get("status", False))

    def test_get_user_transactions(self):
        self.test_purchase_product()
        self.PROD_I += 1
        self.test_purchase_product()
        self.PROD_I -= 1
        user = self.sessions[self.U1]
        purchase_history = self.commerce_system.get_personal_purchase_history(user)
        self.assertTrue(len(purchase_history) == 2)

    def test_get_shop_transactions(self):
        NUM_PRODUCTS = 3
        products_purchased = make_purchases(
            self.commerce_system, self.sessions[self.U1], self.shop_ids[self.SHOP_I],
            self.shop_to_products[self.shop_ids[self.SHOP_I]][:NUM_PRODUCTS]
        )
        transactions = self.commerce_system.get_shop_transactions(
            self.sessions[self.U1], self.shop_ids[self.SHOP_I]
        )
        self.assertTrue(len(transactions) == NUM_PRODUCTS)
        self.assertTrue(
            all(map(lambda pid:
                any(map(lambda t: t["product_id"] == pid,
                    transactions)),
                products_purchased))
        )

    def test_get_system_transactions(self):
        products_purchased = []
        for i in range(3):
            products_purchased.extend(make_purchases(
                self.commerce_system, self.sessions[i], self.shop_ids[i], self.shop_to_products[i]
            ))
        transactions = self.commerce_system.get_system_transactions()
        self.assertTrue(len(transactions) == len(products_purchased))
        self.assertTrue(
            all(map(lambda pid:
                any(map(lambda t: t["product_id"] == pid,
                    transactions)),
                products_purchased))
        )


class TestsWithData(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()


    def test_get_shop_info(self):
        shop_info = self.commerce_system.get_shop_info()

    def test_get_shop_info_bad_shop_id(self):
        self.assertFalse(self.commerce_system.get_shop_info("non_existing_shop_id"))

    def test_search_products_by_name(self):
        pass

    def test_search_products_by_filters(self):
        pass

    def test_search_products_by_name_and_filters(self):
        pass


class ParallelismTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])

    @staticmethod
    def run_parallel_test(f1, f2):
        t1, t2 = th.Thread(target=f1), th.Thread(target=f2)
        t1.start(), t2.start()
        t1.join(), t2.join()

    def test_parallel_purchase_of_last_product(self):
        pass

    def test_parallel_purchase_and_delete_of_product(self):
        pass

    def test_parallel_product_purchase_and_price_change(self):
        pass

    def test_parallel_edit_and_delete_of_product(self):
        # product should be deleted, regardless of whether it was edited or not
        pass

    def test_parallel_appointment_of_user(self):
        # the first one of them will succeed and the other will fail
        pass

    def test_parallel_login_of_same_user(self):
        pass

    def test_parallel_registration_of_users_with_the_same_name(self):
        results = []
        session_id2 = self.commerce_system.enter()

        def u1():
            print("here")
            results.append(self.commerce_system.register(self.session_id, **users[0]))

        def u2():
            print("here2")
            results.append(self.commerce_system.register(session_id2, **users[0]))

        self.run_parallel_test(u1, u2)
        self.assertTrue(any(results))
        self.assertFalse(all(results))


if __name__ == "__main__":
    unittest.main()
