import unittest
from typing import List

from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.tests.mocks import PaymentMock, DeliveryMock, NotificationMock
from domain.authentication_module.authenticator import Authenticator
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.discount_module.discount_management import DiscountDict
from domain.notifications.notifications import Notifications
from domain.payment_module.payment_system import IPaymentsFacade

shop_dict = {"shop_name": "Armani", "description": "dudu faruk's favorite shop"}
shop_dict2 = {"shop_name": "Galavanni", "description": "dudu faruk's second favorite shop"}
product1_dict = {"product_name": "Armani shirt", "price": 299.9, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product2_dict = {"product_name": "Armani Belt", "price": 99.9, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
all_permissions = ["delete_product", "edit_product", "add_product"]
payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
delivery_details = {}


# payment_details = [credit_card_number: int, expiration_date: int, card_holder_name: str, user_name: str]

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        Notifications.set_communication(NotificationMock)
        IPaymentsFacade.get_payment_facade = lambda: PaymentMock(True)
        IDeliveryFacade.get_delivery_facade = lambda: DeliveryMock(True)
        self.facade = CommerceSystemFacade(Authenticator())
        self.user_id1 = self.facade.enter()
        self.user_id2 = self.facade.enter()
        self.username1 = "user1"
        self.username2 = "user2"
        self.password = "123456"
        self.facade.register(self.user_id1, self.username1, self.password)
        self.facade.register(self.user_id2, self.username2, self.password)

    def test_login(self):
        self.assertTrue(self.facade.login(self.user_id1, self.username1, self.password))

    def test_open_shop(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        self.assertGreater(self.facade.open_shop(self.user_id1, **shop_dict), 0)

    def test_add_product(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

    def test_appoint_manager(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        self.facade.get_shop_info(shop_id)
        self.facade.appoint_shop_manager(self.user_id1, shop_id, self.username2, all_permissions)

    def test_add_product2(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        self.facade.get_shop_info(shop_id)
        self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        self.facade.appoint_shop_manager(self.user_id1, shop_id, self.username2, all_permissions)
        self.facade.login(self.user_id2, self.username2, self.password)
        self.facade.add_product_to_shop(self.user_id2, shop_id, **product2_dict)

    def test_delete_product(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        self.facade.get_shop_info(shop_id)
        product_id = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        self.facade.delete_product(self.user_id1, shop_id, product_id)

    def test_not_valid_register1(self):
        un_registered_id = self.facade.enter()
        self.assertRaises(AssertionError, self.facade.register, un_registered_id, self.username1, "123456")

    def test_not_valid_register2(self):
        un_registered_id = self.facade.enter()
        self.assertRaises(AssertionError, self.facade.register, un_registered_id,
                          "new user1", "1234567890123456789012345")

    def test_not_valid_register3(self):
        un_registered_id = self.facade.enter()
        self.assertRaises(AssertionError, self.facade.register, un_registered_id, "new user12345678901234567890",
                          "123456")

    def login_user1_user2_open_shop_and_add_prod(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        return shop_id, product_id1

    def test_purchase_product1(self):  # tests purchase with username supplied
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict, delivery_details)

    def test_purchase_product_more_than_1(self):  # tests purchase more than 1 of the same product
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 2, payment_dict, delivery_details)

    def test_purchase_2_different_products(self):  # tests purchase 2 different products
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict, delivery_details)
        self.facade.purchase_product(self.user_id2, shop_id, product_id2, 1, payment_dict, delivery_details)

    def test_purchase_product_multi_times(self):  # tests purchase the same product few times
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict, delivery_details)
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict, delivery_details)
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict, delivery_details)

    def test_purchase_product_too_large_quantity(self):  # tests purchase product with quantity too big
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()
        self.assertRaises(AssertionError, self.facade.purchase_product, self.user_id2, shop_id, product_id1, 1000,
                          payment_dict, delivery_details)

    def test_purchase_product_with_discount(self):
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()

        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': product_id1, 'percentage': 20, "composite": False
        }
        self.facade.add_discount(self.user_id1, shop_id, False, None, product1_discount_dict1)
        # first user opened shop, added discount on product 1

        buy_quantity1 = 2
        transaction: dict = self.facade.purchase_product(
            self.user_id2, shop_id, product_id1, buy_quantity1, payment_dict, delivery_details
        )

        # checks the discount
        self.assertTrue(transaction["price"] == (100 - product1_discount_dict1['percentage']) / 100
                        * buy_quantity1 * product1_dict['price'])
        # checks removing products from shops stocks
        self.assertTrue(self.facade.get_shop(shop_id).products[product_id1].get_quantity() ==
                        product1_dict['quantity'] - buy_quantity1)
        # checks transaction added
        self.assertTrue(len(self.facade.get_shop(shop_id).transaction_history) == 1)

    def test_purchase_bag_with_discount(self):
        shop_id, product_id1 = self.login_user1_user2_open_shop_and_add_prod()

        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': product_id1, 'percentage': 20, "composite": False
        }
        # first user opened shop, added discount on product 1
        self.facade.add_discount(self.user_id1, shop_id, False, None, product1_discount_dict1)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)

        buy_quantity1 = 1
        buy_quantity2 = 1
        self.facade.save_product_to_cart(self.user_id2, shop_id, product_id1, buy_quantity1)
        self.facade.save_product_to_cart(self.user_id2, shop_id, product_id2, buy_quantity2)

        transaction: dict = self.facade.purchase_shopping_bag(self.user_id2, shop_id, payment_dict, delivery_details)
        trans_price = (round(transaction["price"], 2))
        expected_price = (round((100 - product1_discount_dict1['percentage']) / 100
                                * buy_quantity1 * product1_dict['price'] + product2_dict['price'] * buy_quantity2, 2))

        # checks the discount
        self.assertTrue(trans_price == expected_price)
        # checks removing products from shops stocks
        self.assertTrue(self.facade.get_shop(shop_id).products[product_id1].get_quantity() ==
                        product1_dict['quantity'] - buy_quantity1)
        self.assertTrue(self.facade.get_shop(shop_id).products[product_id2].get_quantity() ==
                        product2_dict['quantity'] - buy_quantity2)
        # checks transaction added
        self.assertTrue(len(self.facade.get_shop(shop_id).transaction_history) == 1)

    def test_purchase_cart_with_discount(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id1 = self.facade.open_shop(self.user_id1, **shop_dict)
        shop1_product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id1, **product1_dict)
        # add shop1_product_id2
        self.facade.add_product_to_shop(self.user_id1, shop_id1, **product2_dict)
        product1_discount_dict1: DiscountDict = {
            'type': 'product', 'identifier': shop1_product_id1, 'percentage': 20, "composite": False
        }
        self.facade.add_discount(self.user_id1, shop_id1, False, None, product1_discount_dict1)
        # first user opened shop1, added discount on product 1

        shop_id2 = self.facade.open_shop(self.user_id1, **shop_dict2)
        # add shop2_product_id1
        self.facade.add_product_to_shop(self.user_id1, shop_id2, **product1_dict)
        shop2_product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id2, **product2_dict)
        product2_discount_dict: DiscountDict = {
            'type': 'product', 'identifier': shop2_product_id2, 'percentage': 20, "composite": False
        }
        self.facade.add_discount(self.user_id1, shop_id2, False, None, product2_discount_dict)
        # first user opened shop2, added discount on product 2

        self.facade.login(self.user_id2, self.username2, self.password)
        buy_quantity1 = 2
        buy_quantity2 = 2
        self.facade.save_product_to_cart(self.user_id2, shop_id1, shop1_product_id1, buy_quantity1)
        self.facade.save_product_to_cart(self.user_id2, shop_id2, shop2_product_id2, buy_quantity2)

        transactions: List[dict] = self.facade.purchase_cart(self.user_id2, payment_dict, delivery_details, True)
        total_price = sum(t["price"] for t in transactions)
        expected_price = (round((100 - product1_discount_dict1['percentage']) / 100
                                * buy_quantity1 * product1_dict['price'] +
                                (100 - product2_discount_dict['percentage']) / 100 * product2_dict[
                                    'price'] * buy_quantity2, 2))
        # checks the discount
        self.assertTrue(total_price == expected_price)
        # checks removing products from shops stocks
        self.assertTrue(self.facade.get_shop(shop_id1).products[shop1_product_id1].get_quantity() ==
                        product1_dict['quantity'] - buy_quantity1)
        self.assertTrue(self.facade.get_shop(shop_id2).products[shop2_product_id2].get_quantity() ==
                        product2_dict['quantity'] - buy_quantity2)
        # checks transaction added
        self.assertTrue(len(self.facade.get_shop(shop_id1).transaction_history) == 1)
        self.assertTrue(len(self.facade.get_shop(shop_id2).transaction_history) == 1)
