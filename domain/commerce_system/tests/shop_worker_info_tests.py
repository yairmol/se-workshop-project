import unittest
from unittest.mock import MagicMock

from domain.commerce_system.appointment import ShopOwner, ShopManager
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import Subscribed


shop_dict = {"shop_name": "s1", "description": "desc"}


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.owner_sub = Subscribed("test sub", "0")
        self.test_shop = Shop(**shop_dict)
        self.owner_app = ShopOwner(self.test_shop)
        self.owner_sub.appointments[self.test_shop] = self.owner_app

    def test_1(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        print("test 1")
        print(str(self.test_shop.get_staff_info()))

    def test_2(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_manager(self.owner_sub, self.test_shop, [])
        new_sub.promote_manager_to_owner(self.owner_sub, self.test_shop)
        print("test 2")
        print(str(self.test_shop.get_staff_info()))

    def test_3(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_manager(self.owner_sub, self.test_shop, [])
        new_sub.un_appoint_manager(self.owner_sub, self.test_shop)
        print("test 3")
        print(str(self.test_shop.get_staff_info()))

    def test_4(self):
        new_sub = Subscribed("new sub1", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        new_sub.un_appoint_owner(self.owner_sub, self.test_shop)
        print("test 4")
        print(str(self.test_shop.get_staff_info()))

    def test_5(self):
        new_sub = Subscribed("new sub1", "0")
        new_sub2 = Subscribed("new sub2", "0")
        app2 = ShopOwner(self.test_shop, self.owner_app)
        new_sub2.appointments[self.test_shop] = app2
        new_sub.appoint_manager(self.owner_sub, self.test_shop, [])
        print("test 5")
        print(str(self.test_shop.get_staff_info()))

    def test_6(self):
        new_sub = Subscribed("new sub1", "0")
        new_sub2 = Subscribed("new sub2", "0")
        new_sub3 = Subscribed("new sub3", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        new_sub2.appoint_owner(new_sub, self.test_shop)
        new_sub3.appoint_owner(new_sub, self.test_shop)
        new_sub.un_appoint_owner(self.owner_sub, self.test_shop)
        print("test 6")
        print(str(self.test_shop.get_staff_info()))
