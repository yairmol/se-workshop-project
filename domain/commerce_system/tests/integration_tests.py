import unittest
from datetime import datetime
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.user import User, Subscribed
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop

shop_dict = {"shop_name": "Armani", "description": "dudu faruk's favorite shop"}
product1_dict = {"product_name": "Armani shirt", "price": 299.9, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product2_dict = {"product_name": "Armani Belt", "price": 99.9, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
all_permissions = ["delete_product", "edit_product", "add_product"]


# payment_details = [foatcredit_card_number: int, expiration_date: int, card_holder_name: str, user_name: str]

class IntegrationTests(unittest.TestCase):

    def setUp(self):

        self.facade = CommerceSystemFacade()
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
        self.assertTrue(self.facade.login(self.user_id1, self.username1, self.password))
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
        self.assertRaises(AssertionError, self.facade.register, un_registered_id, "new user12345678901234567890", "123456")

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
        product_id1 = product_id = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)

    def test_purchase_product3(self):  # tests purchase more than 1 of the same product
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = product_id = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        # credit_card_number = 1234
        # expiration_date = 25
        # card_holder_name = "Dudu"
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 2, payment_dict)

    def test_purchase_product4(self):  # tests purchase 2 different products
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product2_dict)

        self.facade.login(self.user_id2, self.username2, self.password)

        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.facade.purchase_product(self.user_id2, shop_id, product_id1, 1, payment_dict)
        self.facade.purchase_product(self.user_id2, shop_id, product_id2, 1, payment_dict)

    def test_purchase_product5(self):  # tests purchase the same product few times
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

    def test_purchase_product6(self):  # tests purchase product with quantity too big
        self.facade.login(self.user_id1, self.username1, self.password)
        shop_id = self.facade.open_shop(self.user_id1, **shop_dict)
        product_id1 = self.facade.add_product_to_shop(self.user_id1, shop_id, **product1_dict)
        product_id2 = self.facade.add_product_to_shop(self.user_id1, shop_id,
                                                      **product2_dict)

        self.facade.login(self.user_id2, self.username2, self.password)
        payment_dict = {"credit_card_number": 1234, "expiration_date": 25, "car_holder_name": "Dudu"}
        self.assertRaises(AssertionError, self.facade.purchase_product, self.user_id2, shop_id, product_id1, 1000,
                          payment_dict)
