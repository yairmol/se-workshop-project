import unittest
from datetime import datetime
from typing import List

from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import User, Subscribed
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.authentication_module.authenticator import Authenticator
from domain.discount_module.discount_management import DiscountDict

shop_dict = {"shop_name": "Armani", "description": "dudu faruk's favorite shop"}
shop_dict2 = {"shop_name": "Galavanni", "description": "dudu faruk's second favorite shop"}
product1_dict = {"product_name": "Armani shirt", "price": 299.9, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product2_dict = {"product_name": "Armani Belt", "price": 99.9, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
all_permissions = ["delete_product", "edit_product", "add_product"]


# payment_details = [foatcredit_card_number: int, expiration_date: int, card_holder_name: str, user_name: str]

class IntegrationTests(unittest.TestCase):

    def setUp(self):

        self.facade = CommerceSystemFacade(Authenticator())
        self.user_id1 = self.facade.enter()
        self.user_id2 = self.facade.enter()
        self.username1 = "user1"
        self.username2 = "user2"
        self.password = "123456"
        self.facade.register(self.user_id1, self.username1, self.password)
        self.facade.register(self.user_id2, self.username2, self.password)

    def test_login(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            return True
        except AssertionError as e:
            return False

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

    def test_purchase_product1(self):  # tests purchase with username supplied
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)

    def test_purchase_product2(self):  # tests purchase without username supplied
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)

    def test_purchase_product_more_than_1(self):  # tests purchase more than 1 of the same product
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = product_id = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        # credit_card_number = 1234
        # expiration_date = 25
        # card_holder_name = "Dudu"
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 2, payment_dict)

    def test_purchase_2_different_products(self):  # tests purchase 2 different products
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)

        self.facade.login(self.user_id2, self.username2, self.password)

        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)
        self.facade.purchase_product(self.user_id2, shop_id, product_id2, 1, payment_dict)

    def test_purchase_product_multi_times(self):  # tests purchase the same product few times
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)
        self.facade.login(self.user_id2, self.username2, self.password)

        # self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)

    def test_purchase_product_too_large_quantity(self):  # tests purchase product with quantity too big
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id,
                                                      **product2_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.assertRaises(AssertionError, self.facade.purchase_product, self.user_id2, shop_id, product_id1, 1000,
                          payment_dict)

    def test_purchase_product_with_discount(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)
        product1_discount_dict1: DiscountDict = {'type': 'product', 'identifier': product_id1, 'percentage': 20}
        self.facade.add_discount(self.user_id1, shop_id, False, None, product1_discount_dict1)
        # first user opened shop, added discount on product 1

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        quantity = 2
        transaction: Transaction = self.facade.purchase_product(self.user_id2, shop_id, product_id1, quantity, payment_dict)
        assert transaction.price == (100 - product1_discount_dict1['percentage']) / 100 \
               * quantity * product1_dict['price']

    def test_purchase_bag_with_discount(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)
        product1_discount_dict1: DiscountDict = {'type': 'product', 'identifier': product_id1, 'percentage': 20}
        self.facade.add_discount(self.user_id1, shop_id, False, None, product1_discount_dict1)
        # first user opened shop, added discount on product 1

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        quantity1 = 1
        quantity2 = 1
        self.facade.save_product_to_cart(self.user_id2,shop_id,product_id1,1)
        self.facade.save_product_to_cart(self.user_id2, shop_id, product_id2, 1)

        transaction: Transaction = self.facade.purchase_shopping_bag(self.user_id2,shop_id,payment_dict)
        trans_price = (round(transaction.price,2))
        expected_price =(round((100 - product1_discount_dict1['percentage']) / 100 \
               * quantity1 * product1_dict['price'] + product2_dict['price'] * quantity2, 2))

        assert trans_price == expected_price

    def test_purchase_cart_with_discount(self):
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id1 = self.facade.open_shop(self.user_id1, **shop_dict)
        shop1_product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id1, **product1_dict)
        shop1_product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id1, **product2_dict)
        product1_discount_dict1: DiscountDict = {'type': 'product', 'identifier': shop1_product_id1, 'percentage': 20}
        self.facade.add_discount(self.user_id1, shop_id1, False, None, product1_discount_dict1)
        # first user opened shop1, added discount on product 1

        shop_id2 = self.facade.open_shop(self.user_id1, **shop_dict2)
        shop2_product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id2, **product1_dict)
        shop2_product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id2, **product2_dict)
        product2_discount_dict: DiscountDict = {'type': 'product', 'identifier': shop2_product_id2, 'percentage': 20}
        self.facade.add_discount(self.user_id1, shop_id2, False, None, product2_discount_dict)
        # first user opened shop2, added discount on product 2

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        quantity1 = 2
        quantity2 = 2
        self.facade.save_product_to_cart(self.user_id2, shop_id1, shop1_product_id1, quantity1)
        self.facade.save_product_to_cart(self.user_id2, shop_id2, shop2_product_id2, quantity2)

        transactions: List[Transaction] = self.facade.purchase_cart(self.user_id2, payment_dict, True)
        total_price = sum(t.price for t in transactions)
        expected_price = (round((100 - product1_discount_dict1['percentage']) / 100 \
                                * quantity1 * product1_dict['price'] +
                                (100 - product2_discount_dict['percentage']) / 100 * product2_dict['price'] * quantity2, 2))

        assert total_price == expected_price
