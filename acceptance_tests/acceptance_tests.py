import unittest
from unittest import TestCase
import threading as th

from domain.discount_module.discount_management import DiscountDict, SimpleCond
from driver import Driver
from test_data import users, shops, products, permissions, payment_details, simple_condition_dict
from test_utils import (
    enter_register_and_login, add_product, make_purchases, register_login_users,
    open_shops, add_products, appoint_owners_and_managers, shop_to_products,
    sessions_to_shops, get_shops_not_owned_by_user, fill_with_data, admin_login, get_credentials
)
from data_model import (
    UserModel as Um, ProductModel as Pm, ConditionsModel as Cm,
    PermissionsModel as PermM,
)


# 2. Guest Functional Requirements tests
class GuestTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.session_id = self.commerce_system.enter()['result']
        self.assertIsInstance(self.session_id, str)
        self.assertNotEqual(self.session_id, "")

    def tearDown(self) -> None:
        status = self.commerce_system.exit(self.session_id)['status']
        self.assertTrue(status)
        self.commerce_system.cleanup()

    # 2.1 enter + 2.2 exit
    def test_enter_exit(self):
        self.assertTrue(True)

    # 2.3 register
    def test_registration_simple(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0])['status'])

    # 2.3 register
    def test_registration_with_empty_credentials(self):
        u = {Um.USERNAME: "", Um.EMAIL: "", Um.PASSWORD: "password24tgf"}
        self.assertFalse(self.commerce_system.register(self.session_id, **u)['status'])

    # 2.3 register
    def test_registration_with_existing_email_or_username(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0])['status'])
        user2 = users[0].copy()
        user2[Um.USERNAME] = users[0][Um.USERNAME]
        self.assertFalse(self.commerce_system.register(self.session_id, **user2)['status'])

    # 2.4 login
    def test_login_successful(self):
        self.assertTrue(self.commerce_system.register(self.session_id, **users[0])['status'])
        self.assertTrue(self.commerce_system.login(self.session_id, **get_credentials(users[0]))['status'])

    # 2.4 login
    def test_login_failed(self):
        # user hasn't registered yet
        self.assertFalse(self.commerce_system.login(self.session_id, **get_credentials(users[0]))['status'])

    # 2.4 login
    def test_login_failed_bad_credentials(self):
        user = users[0].copy()
        self.assertTrue(self.commerce_system.register(self.session_id, **user)['status'])
        user[Um.PASSWORD] = "pasSwordd"
        self.assertFalse(self.commerce_system.login(self.session_id, **get_credentials(user))['status'])

    # 2.4 login
    def test_logout_without_login(self):
        self.assertFalse(self.commerce_system.logout(self.session_id)['status'])

    # 3.2 open shop
    def test_guest_cant_open_shop(self):
        # try to open shop as guest
        self.assertFalse(self.commerce_system.open_shop(self.session_id, **shops[0])['status'])

    # 3.7 get transactions
    def test_guest_cant_get_transactions(self):
        self.assertFalse(self.commerce_system.get_personal_purchase_history(self.session_id)['status'])


class SubscribedTests(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])

    def tearDown(self) -> None:
        self.assertTrue(self.commerce_system.logout(self.session_id)['status'])
        status = self.commerce_system.exit(self.session_id)['status']
        self.assertTrue(status)
        self.commerce_system.cleanup()

    # 3.1 logout
    def test_logout(self):
        # setUp and tearDown will perform the login and logout
        self.assertTrue(True)

    # 3.1 logout
    def test_logout_bad_session_id(self):
        self.commerce_system.logout("non_existing_session_id")

    # 3.2 open shop
    def test_open_shop(self):
        shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])['result']
        self.assertIsInstance(shop_id, int)
        self.assertGreater(shop_id, 0)

    # 3.2 open shop
    def test_open_shop_with_existing_name(self):
        self.assertGreater(self.commerce_system.open_shop(self.session_id, **shops[0])['result'], 0)
        self.assertFalse(self.commerce_system.open_shop(self.session_id, **shops[0])['status'])

    # 2.3 register
    def test_register_when_logged_in(self):
        self.assertFalse(self.commerce_system.register(
            self.session_id, **users[2]
        )['status'])


class ShopOwnerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.session_id, **shops[0])['result']
        self.assertIsInstance(self.shop_id, int)
        self.assertGreater(self.shop_id, 0)

    def tearDown(self) -> None:
        self.commerce_system.cleanup()

    # 4.1 add product to shop
    def test_add_product_to_shop(self):
        self.assertGreater(
            add_product(self.session_id, self.commerce_system, self.shop_id, products[0]), 0)

    # 4.1 edit product in shop
    def test_edit_product_in_shop(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        p = products[0].copy()
        p[Pm.PRODUCT_ID] = prod_id
        self.assertTrue(self.commerce_system.edit_product_info(self.session_id, self.shop_id, **p)['status'])

    # 4.1 edit product in shop
    def test_edit_non_existing_product_in_shop(self):
        p = products[0].copy()
        p[Pm.PRODUCT_ID] = "some_non_existing_id"
        self.assertFalse(self.commerce_system.edit_product_info(
            self.session_id, self.shop_id, **p
        )['status'])

    # 4.1 delete product from shop
    def test_delete_product_from_shop(self):
        prod_id = add_product(
            self.session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.assertTrue(self.commerce_system.delete_product(
            self.session_id, self.shop_id, prod_id
        )['status'])

    # 4.1 delete product from shop
    def test_delete_non_existing_product(self):
        self.assertFalse(self.commerce_system.delete_product(
            self.session_id, self.shop_id, "39r3jrn"
        )['status'])

    # 4.3 appoint shop owner
    def test_appoint_shop_owner(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])

    # 4.3 appoint shop owner
    def test_appoint_owner_by_non_owner(self):
        other_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.appoint_shop_owner(
            other_session_id, self.shop_id, users[0][Um.USERNAME]
        )['status'])

    # 4.3 appoint shop owner
    def test_appoint_owner_already_appointed(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])
        self.assertFalse(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])

    # 4.5 appoint shop manager
    def test_appoint_shop_manager(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )['status'])

    # 4.5 appoint shop manager
    def test_appoint_manager_by_non_owner(self):
        other_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.appoint_shop_manager(
            other_session_id, self.shop_id, users[0][Um.USERNAME], permissions[0]
        )['status'])

    # 4.7 unappoint shop manager
    def test_unappoint_shop_manager(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )['status'])
        self.assertTrue(self.commerce_system.un_appoint_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])

    # 4.7 appoint shop manager
    def test_unappoint_shop_manager_by_non_appointer(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )['status'])
        u2_session_id = enter_register_and_login(self.commerce_system, users[2])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[2][Um.USERNAME]
        )['status'])
        # check that user2 which is a shop owner is not able to unappoint user1
        # which is a shop manager appointed by user0
        self.assertFalse(self.commerce_system.un_appoint_manager(
            u2_session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])

    # 4.3 appoint shop owner
    def test_unappoint_shop_owner_by_non_owner(self):
        # the user trying to unappoint the worker is not a shop owner/manager
        u_session_id = enter_register_and_login(self.commerce_system, users[1])
        enter_register_and_login(self.commerce_system, users[2])
        self.assertFalse(self.commerce_system.un_appoint_shop_owner(
            u_session_id, self.shop_id, users[2][Um.USERNAME]
        )['status'])

    # 4.3 appoint shop owner
    def test_appoint_manager_to_owner(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )['status'])
        self.assertTrue(self.commerce_system.promote_shop_owner(
            self.session_id, self.shop_id, users[1][Um.USERNAME]
        )['status'])

    # 4.9 get staff
    def test_get_shop_staff(self):
        enter_register_and_login(self.commerce_system, users[1])
        self.assertTrue(self.commerce_system.appoint_shop_manager(
            self.session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )['status'])
        enter_register_and_login(self.commerce_system, users[2])
        self.assertTrue(self.commerce_system.appoint_shop_owner(
            self.session_id, self.shop_id, users[2][Um.USERNAME]
        )['status'])
        shop_staff_res = self.commerce_system.get_shop_staff_info(self.session_id, self.shop_id)
        self.assertTrue(shop_staff_res["status"])
        shop_staff = shop_staff_res["result"]
        expected_usernames = {u[Um.USERNAME] for u in users[:3]}
        self.assertEqual(len(shop_staff), len(expected_usernames))
        usernames_got = {u[Um.USERNAME] for u in shop_staff}
        self.assertEqual(expected_usernames, usernames_got)

    # 4.9 get staff
    def test_get_shop_staff_by_non_owner(self):
        non_owner = enter_register_and_login(self.commerce_system, users[1])
        self.assertFalse(self.commerce_system.get_shop_staff_info(non_owner, self.shop_id)['status'])


class ShopManagerOperations(TestCase):

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.owner_session_id = enter_register_and_login(self.commerce_system, users[0])
        self.shop_id = self.commerce_system.open_shop(self.owner_session_id, **shops[0])['result']
        self.manager_session_id = enter_register_and_login(self.commerce_system, users[1])
        self.manager_username = users[1][Um.USERNAME]
        self.commerce_system.appoint_shop_manager(
            self.owner_session_id, self.shop_id, users[1][Um.USERNAME], permissions[0]
        )

    def tearDown(self) -> None:
        self.commerce_system.cleanup()

    # 4.6 edit manager permissions
    def edit_manager_permissions(self, m_permissions):
        self.assertTrue(self.commerce_system.edit_manager_permissions(
            self.owner_session_id, self.shop_id, self.manager_username, m_permissions
        )['status'])

    # 4.1 add product to shop
    def test_add_product_to_shop(self):
        self.assertGreater(
            add_product(self.manager_session_id, self.commerce_system, self.shop_id, products[0]),
            0
        )

    # 4.1 add product to shop + 5.1 manager permissions
    def test_add_product_to_shop_no_permissions(self):
        self.edit_manager_permissions([])
        self.assertRaises(
            AssertionError, add_product,
            self.manager_session_id, self.commerce_system, self.shop_id, products[0]
        )

    # 4.1 edit product in shop + 5.1 manager permissions
    def test_edit_product_in_shop(self):
        prod_id = add_product(
            self.manager_session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.assertGreater(prod_id, 0)
        p = products[0].copy()
        p[Pm.PRODUCT_ID] = prod_id
        self.assertTrue(self.commerce_system.edit_product_info(
            self.manager_session_id, self.shop_id, **p
        )['status'])

    # 4.1 edit product in shop + 5.1 manager permissions
    def test_edit_product_in_shop_no_permission(self):
        prod_id = add_product(
            self.owner_session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.assertGreater(prod_id, 0)
        p = products[0].copy()
        p[Pm.PRODUCT_ID] = prod_id
        self.edit_manager_permissions([])
        self.assertFalse(self.commerce_system.edit_product_info(
            self.manager_session_id, self.shop_id, **p
        )['status'])

    # 4.1 delete product from shop + 5.1 manager permissions
    def test_delete_product_from_shop(self):
        prod_id = add_product(
            self.manager_session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.assertTrue(self.commerce_system.delete_product(
            self.manager_session_id, self.shop_id, prod_id
        )['status'])

    # 4.1 delete product from shop + 5.1 manager permissions
    def test_delete_product_from_shop_no_permission(self):
        prod_id = add_product(
            self.manager_session_id, self.commerce_system, self.shop_id, products[0]
        )
        self.edit_manager_permissions([])
        self.assertFalse(self.commerce_system.delete_product(
            self.manager_session_id, self.shop_id, prod_id
        )['status'])

    # 4.2.1 manage discounts
    def test_add_discount_with_no_cond(self):
        perm = [PermM.ADD_PRODUCT_PERM, PermM.MANAGE_DISCOUNT_PERM]
        self.assertTrue(self.commerce_system.edit_manager_permissions(
            self.owner_session_id, self.shop_id, self.manager_username, perm)['status'])

        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': 1, 'percentage': 20, "composite": False
        }
        ret = self.commerce_system.add_discount(
            self.manager_session_id, self.shop_id, False, None, product1_discount_dict1
        )
        self.assertTrue(ret["status"])

    def add_discount_with_cond(self, session):
        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': 1, 'percentage': 20, "composite": False
        }
        simple_cond: SimpleCond = {'condition': 'sum', 'type': 'shop', 'identifier': 'shop', 'num': 50}
        condition = [simple_cond]
        self.assertTrue(self.commerce_system.add_discount(
            session, self.shop_id, True, condition, product1_discount_dict1
        )['status'])

    # 4.2.1 manage discounts
    def test_add_discount_with_cond(self):
        perm = [PermM.ADD_PRODUCT_PERM, PermM.MANAGE_DISCOUNT_PERM]
        self.assertTrue(self.commerce_system.edit_manager_permissions(
            self.owner_session_id, self.shop_id, self.manager_username, perm)['status'])
        self.add_discount_with_cond(self.manager_session_id)

    # 4.2.1 manage discounts
    def test_delete_discount(self):
        self.add_discount_with_cond(self.owner_session_id)
        self.assertTrue(self.commerce_system.delete_discounts(self.owner_session_id, self.shop_id, [1])['status'])

    # 4.2.1 manage discounts
    def test_aggregate_discounts(self):
        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': 1, 'percentage': 20, "composite": False
        }
        discount_dict2: DiscountDict = {'type': 'shop', 'identifier': 'shop', 'percentage': 15, "composite": False}

        simple_cond: SimpleCond = {'condition': 'sum', 'type': 'shop', 'identifier': 'shop', 'num': 50}
        condition = [simple_cond]
        add1_dict = self.commerce_system.add_discount(self.owner_session_id,
                                                      self.shop_id, False, None, product1_discount_dict1)
        add2_dict = self.commerce_system.add_discount(self.owner_session_id,
                                                      self.shop_id, True, condition, discount_dict2)
        self.assertTrue(add1_dict['status'])
        self.assertTrue(add2_dict['status'])
        disc_id1 = add1_dict['result']
        disc_id2 = add2_dict['result']
        self.assertTrue(self.commerce_system.aggregate_discounts(self.owner_session_id, self.shop_id,
                                                                 [disc_id1, disc_id2], 'max')['status'])


class PurchasesTests(TestCase):
    NUM_USERS = len(users)
    NUM_SHOPS = len(shops)
    NUM_PRODUCTS = len(products)
    U1, U2 = 0, 1

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.sessions_to_users = register_login_users(self.commerce_system, self.NUM_USERS)
        self.sessions = list(self.sessions_to_users.keys())
        self.shop_id_to_shop, self.shop_to_opener = open_shops(self.commerce_system, self.sessions, self.NUM_SHOPS)
        self.shop_ids = list(self.shop_id_to_shop.keys())
        self.product_to_shop = add_products(self.commerce_system, self.shop_to_opener, self.shop_ids, self.NUM_PRODUCTS)
        self.shop_to_owners, self.shop_to_managers = appoint_owners_and_managers(
            self.commerce_system, self.sessions, self.sessions_to_users, self.shop_ids
        )
        self.shops_to_products = shop_to_products(self.product_to_shop, self.shop_ids)
        self.shop_to_staff, self.session_to_shops = sessions_to_shops(
            self.shop_to_opener, self.shop_to_owners, self.shops_to_products, self.sessions
        )

    def tearDown(self) -> None:
        self.commerce_system.cleanup()

    # 2.7 save product to cart
    def test_save_product_to_cart(self):
        user_session = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(user_session, self.shop_ids, self.shop_to_staff)[0]
        product_id = self.shops_to_products[shop_id][0]
        self.assertTrue(self.commerce_system.save_product_to_cart(user_session, shop_id, product_id, 1)['status'])

    # 2.7 save product to cart
    def test_save_non_existing_product_to_cart(self):
        user = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(user, self.shop_ids, self.shop_to_staff)[0]
        self.assertFalse(self.commerce_system.save_product_to_cart(
            self.sessions[self.U1], shop_id, "some_non_existing_product_id", 1
        )['status'])

    # 2.8 get cart info
    def test_get_cart_info(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        prod_id = self.shops_to_products[shop_id][0]
        self.assertTrue(self.commerce_system.save_product_to_cart(u1, shop_id, prod_id, 1)['status'])
        cart_info = self.commerce_system.get_cart_info(u1)['result']
        self.assertTrue(shop_id in cart_info["shopping_bags"])
        self.assertEqual(len(cart_info["shopping_bags"].items()), 1)
        self.assertTrue(
            any(map(lambda p: p[Pm.PRODUCT_ID] == prod_id, cart_info["shopping_bags"][shop_id]["products"])))

    # 2.9 purchase product
    def test_purchase_product(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        prod_id = self.shops_to_products[shop_id][0]
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 2.9 purchase cart
    def test_purchase_cart(self):
        num_prods = 4
        u1 = self.sessions[self.U1]
        shops1 = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)
        prods = []
        for shop in shops1:
            prods += self.shops_to_products[shop]
        self.assertTrue(all(map(lambda p: self.commerce_system.save_product_to_cart(
            u1, self.product_to_shop[p], p, 1
        ), prods[:num_prods])))
        self.assertTrue(self.commerce_system.purchase_cart(u1, payment_details[0], {})['status'])

    def make_purchases_and_check_transactions(self, u1, prods, num_prods):
        make_purchases(self.commerce_system, u1, self.product_to_shop, prods[:num_prods])
        transaction_history = self.commerce_system.get_personal_purchase_history(u1)['result']
        self.assertEqual(len(transaction_history), num_prods)
        self.assertTrue(
            all(map(lambda pr:
                    any(map(lambda t: pr == t["products"][0]["product_id"],
                            transaction_history)),
                    prods[:num_prods]))
        )

    # 3.7 get transaction
    def test_get_user_transactions(self):
        num_prods = 3
        u1 = self.sessions[self.U1]
        shops1 = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)
        prods = []
        for shop in shops1:
            prods += self.shops_to_products[shop]
        self.make_purchases_and_check_transactions(u1, prods, num_prods)

    # 4.9 get shop transactions
    def test_get_shop_transactions(self):
        num_prods = 3
        u1 = self.sessions[self.U1]
        u2 = self.sessions[self.U2]
        shop_id = list(
            set(get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)) &
            set(get_shops_not_owned_by_user(u2, self.shop_ids, self.shop_to_staff))
        )[0]
        prods = self.shops_to_products[shop_id]
        self.assertTrue(make_purchases(self.commerce_system, u1, self.product_to_shop, prods[:2]))
        self.assertTrue(make_purchases(self.commerce_system, u2, self.product_to_shop, prods[2:num_prods]))
        transactions = self.commerce_system.get_shop_transaction_history(
            self.shop_to_opener[shop_id], shop_id
        )["result"]
        self.assertTrue(len(transactions) == num_prods)
        self.assertTrue(
            all(map(lambda pid:
                    any(map(lambda t: t["products"][0]["product_id"] == pid,
                            transactions)),
                    prods[:num_prods]))
        )

    # 6.4 get system transaction
    def test_get_system_transactions(self):
        products_purchased = []
        for i in range(self.NUM_USERS):
            u = self.sessions[i]
            shop_id = get_shops_not_owned_by_user(u, self.shop_ids, self.shop_to_staff)[0]
            prods = self.shops_to_products[shop_id][:2]
            self.assertTrue(make_purchases(self.commerce_system, u, self.product_to_shop, prods))
            products_purchased.extend(prods)
        admin_session = admin_login(self.commerce_system)
        transactions = self.commerce_system.get_system_transactions(admin_session)["result"]
        self.assertTrue(len(transactions), len(products_purchased))
        self.assertTrue(
            all(map(lambda pid:
                    any(map(lambda t: t["products"][0]["product_id"] == pid,
                            transactions)),
                    products_purchased))
        )

    # PurchasesWithConditionsTests(TestCase):

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_with_max_quantity_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.MAX_QUANTITY_FOR_PRODUCT, Cm.MAX_QUANTITY: 3, Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_that_fails_max_quantity_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.MAX_QUANTITY_FOR_PRODUCT, Cm.MAX_QUANTITY: 3, Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 5, payment_details[0], {}
        )
        self.assertFalse(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_with_time_window_for_product_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_PRODUCT, Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:00',
                          Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_that_fails_time_window_for_product_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_PRODUCT, Cm.MIN_TIME: '00:00',
                          Cm.MAX_TIME: '1:00', Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertFalse(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_with_date_window_for_product_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_PRODUCT, Cm.MIN_DATE: '1/5/2021',
                          Cm.MAX_DATE: '30/5/2021', Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_that_fails_date_window_for_product_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_PRODUCT,
                          Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '3/5/2021', Cm.PRODUCT: prod_id}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertFalse(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_with_time_window_for_category_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_CATEGORY,
                          Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:00', Cm.CATEGORY: "c1"}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_that_fails_time_window_for_category_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_CATEGORY,
                          Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '1:00', Cm.CATEGORY: "c1"}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertFalse(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_with_date_window_for_category_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_CATEGORY,
                          Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '30/5/2021', Cm.CATEGORY: "c1"}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertTrue(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_product_that_fails_date_window_for_category_condition(self):
        u1 = self.sessions[self.U1]
        shop_id = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)[0]
        shop_owner = self.shop_to_owners[shop_id]
        prod_id = self.shops_to_products[shop_id][0]
        condition_dict = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_CATEGORY,
                          Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '3/5/2021', Cm.CATEGORY: "c1"}
        self.assertTrue(self.commerce_system.add_purchase_condition
                        (shop_owner, shop_id, **condition_dict)['status'])
        transaction_status = self.commerce_system.purchase_product(
            u1, shop_id, prod_id, 1, payment_details[0], {}
        )
        self.assertFalse(transaction_status["status"])

    # 4.2.2 manage purchase policies + 2.9 purchase product
    def test_purchase_cart_with_condition(self):
        num_prods = 4
        u1 = self.sessions[self.U1]
        shops1 = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)
        prods = []
        for shop in shops1:
            prods += self.shops_to_products[shop]
            owner = self.shop_to_owners[shop]
            self.assertTrue(
                self.commerce_system.add_purchase_condition(owner, shop, **simple_condition_dict)['status']
            )
        self.assertTrue(all(map(lambda p: self.commerce_system.save_product_to_cart(
            u1, self.product_to_shop[p], p, 1
        ), prods[:num_prods])))
        self.assertTrue(self.commerce_system.purchase_cart(u1, payment_details[0], {})['status'])

    def test_purchase_cart_with_complex_conditions(self):
        num_prods = 4
        u1 = self.sessions[self.U1]
        shops1 = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)
        prods = []
        condition_dict1 = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_CATEGORY,
                           Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '20/7/2021', Cm.CATEGORY: "c1"}
        condition_dict2 = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_CATEGORY,
                           Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:59', Cm.CATEGORY: "c1"}
        condition_dict3 = {Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_CATEGORY,
                           Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '1/5/2021', Cm.CATEGORY: "c1"}
        condition_dict4 = {Cm.CONDITION_TYPE: Cm.TIME_WINDOW_FOR_CATEGORY,
                           Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '00:01', Cm.CATEGORY: "c1"}
        success_and_condition_dict = {Cm.CONDITION_TYPE: Cm.AND,
                                      Cm.CONDITIONS: [condition_dict1, condition_dict2]}
        success_or_condition_dict = {Cm.CONDITION_TYPE: Cm.OR,
                                     Cm.CONDITIONS: [condition_dict3, condition_dict4, condition_dict1]}

        for shop in shops1:
            prods += self.shops_to_products[shop]
            owner = self.shop_to_owners[shop]
            self.assertTrue(self.commerce_system.add_purchase_condition
                            (owner, shop, **success_and_condition_dict)['status'])
            self.assertTrue(self.commerce_system.add_purchase_condition
                            (owner, shop, **success_or_condition_dict)['status'])
        self.assertTrue(all(map(lambda p: self.commerce_system.save_product_to_cart(
            u1, self.product_to_shop[p], p, 1
        ), prods[:num_prods])))
        self.assertTrue(self.commerce_system.purchase_cart(u1, payment_details[0], {})['status'])

    # 3.7 get transactions
    def test_get_user_transactions_with_condition(self):
        num_prods = 3
        u1 = self.sessions[self.U1]
        shops1 = get_shops_not_owned_by_user(u1, self.shop_ids, self.shop_to_staff)
        prods = []
        for shop in shops1:
            prods += self.shops_to_products[shop]
            owner = self.shop_to_owners[shop]
            self.assertTrue(self.commerce_system.add_purchase_condition
                            (owner, shop, **simple_condition_dict)['status'])
        self.make_purchases_and_check_transactions(u1, prods, num_prods)


class GuestTestsWithData(TestCase):
    NUM_USERS = len(users)
    NUM_GUESTS = 3
    NUM_SUBS = NUM_USERS - NUM_GUESTS
    NUM_SHOPS = len(shops)
    NUM_PRODUCTS = len(products)

    U1 = 0
    S1 = 0

    def setUp(self):
        self.commerce_system = Driver.get_system_service()
        self.guest_sess, self.subs_sess, self.sids_to_shop, self.sid_to_sess, self.pid_to_sid = fill_with_data(
            self.commerce_system, self.NUM_GUESTS, self.NUM_SUBS, self.NUM_SHOPS, self.NUM_PRODUCTS
        )
        self.sids = list(self.sids_to_shop.keys())

    def tearDown(self) -> None:
        self.commerce_system.cleanup()

    # 2.5 get shop info
    def test_get_shop_info(self):
        s1 = self.sids[self.S1]
        shop_info = self.commerce_system.get_shop_info(self.guest_sess[self.U1], s1)['result']
        self.assertNotEqual(shop_info, {})
        self.assertEqual(shop_info["shop_name"], self.sids_to_shop[s1]["shop_name"])
        self.assertEqual(len(shop_info["products"]), len([pid for pid, sid in self.pid_to_sid.items() if sid == s1]))

    # 2.5 get shop info
    def test_get_shop_info_bad_shop_id(self):
        self.assertFalse(self.commerce_system.get_shop_info(self.subs_sess[0], "non_existing_shop_id")['status'])

    # 2.6 search products
    def test_search_products_by_name_simple(self):
        results = self.commerce_system.search_products(self.guest_sess[0], product_name=products[0]["product_name"])[
            'result']
        self.assertTrue(len(results) == 1)
        self.assertTrue(results[0]["product_name"] == products[0]["product_name"])

    # 2.6 search products
    def test_search_product_by_name_general(self):
        results = self.commerce_system.search_products(self.guest_sess[0], product_name="p")['result']
        self.assertTrue(len(results) == 0)

    # 2.6 search products
    def test_search_products_by_filters(self):
        results = self.commerce_system.search_products(self.guest_sess[0], filters=[
            {"type": "price_range", "from": 0, "to": 100}
        ])['result']
        products_in_range_indices = [0, 1, 2, 3, 4, 8, 9, 11]
        self.assertTrue(len(results) == len(products_in_range_indices))
        self.assertTrue(
            all(map(lambda p_i:
                    any(map(lambda r: products[p_i]["product_name"] == r["product_name"],
                            results)),
                    products_in_range_indices))
        )

    # 2.6 search products
    def test_search_products_by_name_and_filters(self):
        other_products = [
            {Pm.PRODUCT_NAME: "bamba", Pm.PRODUCT_DESC: "peanuts snack", Pm.PRICE: 5, Pm.QUANTITY: 10},
            {Pm.PRODUCT_NAME: "barbi", Pm.PRODUCT_DESC: "kids doll", Pm.PRICE: 50, Pm.QUANTITY: 10},
            {Pm.PRODUCT_NAME: "bisly", Pm.PRODUCT_DESC: "crunchy snack", Pm.PRICE: 5, Pm.QUANTITY: 10},
        ]
        self.assertTrue(all(map(lambda p: add_product(
            self.sid_to_sess[self.sids[self.S1]], self.commerce_system, self.sids[self.S1], p
        ), other_products)))
        results = self.commerce_system.search_products(self.guest_sess[0], product_name="bambaa", filters=[
            {"type": "price_range", "from": 5, "to": 5}
        ])["result"]
        self.assertTrue(len(results) == 1)
        self.assertTrue(results[0]["product_name"] == "bamba")


class ParallelismTests(TestCase):
    NUM_USERS = len(users)
    NUM_SHOPS = len(shops)
    NUM_PRODUCTS = len(products)

    U1 = 0
    S1 = 0

    def setUp(self) -> None:
        self.commerce_system = Driver.get_system_service()
        self.sess_to_user = register_login_users(self.commerce_system, self.NUM_USERS)
        self.sessions = list(self.sess_to_user.keys())
        self.sid_to_shop, self.sid_to_sess = open_shops(self.commerce_system, self.sessions, 2)
        self.sids = list(self.sid_to_shop.keys())

    def tearDown(self) -> None:
        self.commerce_system.cleanup()

    @staticmethod
    def run_parallel_test(f1, f2):
        t1, t2 = th.Thread(target=f1), th.Thread(target=f2)
        t1.start(), t2.start()
        t1.join(), t2.join()

    def test_parallel_purchase_of_last_product(self):
        num_runs = 10
        p = products[0].copy()
        p["quantity"] = 1
        sid = self.sids[0]
        u_opener = self.sid_to_sess[sid]
        u_buyer1, u_buyer2 = tuple([u for u in self.sessions if u != u_opener])[:2]

        for i in range(num_runs):
            pid = add_product(
                u_opener, self.commerce_system, sid, p
            )
            results = []

            def buyer1():
                results.append(
                    self.commerce_system.purchase_product(u_buyer1, sid, pid, 1, payment_details[0], {})["status"])

            def buyer2():
                results.append(
                    self.commerce_system.purchase_product(u_buyer2, sid, pid, 1, payment_details[0], {})["status"])

            self.run_parallel_test(buyer1, buyer2)
            self.assertTrue(any(results))
            self.assertFalse(all(results))
            results.clear()
            self.commerce_system.delete_product(u_opener, sid, pid)

    def test_parallel_purchase_and_delete_of_product(self):
        num_runs = 10
        p = products[0].copy()
        sid = self.sids[0]
        u_opener = self.sid_to_sess[sid]
        u_buyer = [u for u in self.sessions if u != u_opener][0]

        for i in range(num_runs):
            pid = add_product(
                u_opener, self.commerce_system, sid, p
            )
            results = {}

            def buyer():
                results[u_buyer] = self.commerce_system.purchase_product(u_buyer, sid, pid, 1, payment_details, {})

            def opener():
                results[u_opener] = self.commerce_system.delete_product(u_opener, sid, pid)

            self.run_parallel_test(buyer, opener)
            self.assertTrue(any(results.values()))
            self.commerce_system.remove_product_from_cart(u_opener, sid, pid, 1)

    def test_parallel_registration_of_users_with_the_same_name(self):
        results = []
        sess1, sess2 = self.commerce_system.enter()['result'], self.commerce_system.enter()['result']
        user = {Um.USERNAME: "u1", Um.PASSWORD: "password"}

        def u1():
            results.append(self.commerce_system.register(sess1, **user)['status'])

        def u2():
            results.append(self.commerce_system.register(sess2, **user)['status'])

        self.run_parallel_test(u1, u2)
        self.assertTrue(any(results))
        self.assertFalse(all(results))


if __name__ == "__main__":
    unittest.main()
