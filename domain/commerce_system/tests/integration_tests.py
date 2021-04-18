import unittest
from datetime import datetime
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.user import User, Subscribed
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop

shop_dict = {"shop_name": "Armani", "description": "dudu faruk's favorite shop"}
product1_dict = {"product_name": "Armani shirt", "price": 299.9, "description": "black shirt", "quantity": 5}
product2_dict = {"product_name": "Armani Belt", "price": 99.9, "description": "black belt", "quantity": 10}
all_permissions = ["delete_product", "edit_product", "add_product"]


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

    def test_1(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            return True
        except AssertionError as e:
            return False

    def test_2(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            self.facade.open_shop(self.user_id1, shop_dict)
            return True
        except AssertionError as e:
            return False

    def test_3(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            shop_id = self.facade.open_shop(self.user_id1, shop_dict)
            self.facade.get_shop_info(shop_id)
            self.facade.add_product_to_shop(self.user_id1, shop_id, product1_dict)
            self.facade.add_product_to_shop(self.user_id1, shop_id, product2_dict)
            return True
        except AssertionError as e:
            return False

    def test_4(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            shop_id = self.facade.open_shop(self.user_id1, shop_dict)
            self.facade.get_shop_info(shop_id)
            self.facade.add_product_to_shop(self.user_id1, shop_id, product1_dict)
            self.facade.add_product_to_shop(self.user_id1, shop_id, product2_dict)
            self.facade.appoint_shop_manager(self.user_id1, shop_id, self.username2, all_permissions)
            return True
        except AssertionError as e:
            return False

    def test_5(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            shop_id = self.facade.open_shop(self.user_id1, shop_dict)
            self.facade.get_shop_info(shop_id)
            self.facade.add_product_to_shop(self.user_id1, shop_id, product1_dict)
            self.facade.appoint_shop_manager(self.user_id1, shop_id, self.username2, all_permissions)
            self.facade.add_product_to_shop(self.user_id2, shop_id, product2_dict)
            return True
        except AssertionError as e:
            return False

    def test_6(self):
        try:
            self.facade.login(self.user_id1, self.username1, self.password)
            shop_id = self.facade.open_shop(self.user_id1, shop_dict)
            self.facade.get_shop_info(shop_id)
            product_id = self.facade.add_product_to_shop(self.user_id1, shop_id, product1_dict)
            self.facade.delete_product(self.user_id1,shop_id,product_id)
            return True
        except AssertionError as e:
            return False

    # SHOP_ID = 1
    # PROD_ID = 1
    #
    # def test_get_shop_dict(self):
    #     my_shop_dict = shop_dict.copy()
    #     shop = Shop(shop_id=self.SHOP_ID, **shop_dict)
    #     shop.add_product(Product(self.PROD_ID, **product_dict))
    #     my_product_dict = product_dict.copy()
    #     my_product_dict["product_id"] = self.PROD_ID
    #     my_shop_dict["shop_id"] = self.SHOP_ID
    #     my_shop_dict["products"] = [my_product_dict]
    #     self.assertEquals(my_shop_dict, shop.to_dict())
    #
    # def test_get_shop_info(self):
    #     facade = CommerceSystemFacade()
    #     facade.shops[self.SHOP_ID] = Shop(shop_id=self.SHOP_ID, **shop_dict)
    #     my_shop_dict = shop_dict.copy()
    #     my_shop_dict["shop_id"] = self.SHOP_ID
    #     my_shop_dict["products"] = []
    #     self.assertEquals(facade.get_shop_info(self.SHOP_ID), my_shop_dict)
