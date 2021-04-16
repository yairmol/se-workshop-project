import unittest
from unittest.mock import MagicMock

from domain.commerce_system.appointment import ShopOwner, ShopManager
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.subscribed import Subscribed


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.owner_sub = Subscribed("test sub", "0")
        self.test_shop = Shop(1)
        self.owner_app = ShopOwner(self.test_shop)
        self.owner_sub.appointments[self.test_shop] = self.owner_app

    def test_add_appointment(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        assert self.test_shop in new_sub.appointments.keys()
        assert isinstance(new_sub.appointments[self.test_shop], ShopOwner)
        try:
            new_shop = Shop(2)
            new_sub.appoint_owner(self.owner_sub, new_shop)
            assert False
        except Exception as e:
            pass

    def test_remove_manager(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_manager(self.owner_sub, self.test_shop, [])
        new_sub.un_appoint_manager(self.owner_sub, self.test_shop)
        assert self.test_shop not in new_sub.appointments.keys()
        try:
            new_shop = Shop(2)
            test_owner_2 = ShopOwner(new_shop)
            new_sub_2 = Subscribed("new sub 2", "0")
            new_sub_2.appointments[new_shop] = test_owner_2
            new_sub.appoint_manager(new_sub_2, new_shop, [])
            new_sub.un_appoint_manager(self.owner_sub, new_shop)
            assert False
        except Exception as e:
            pass

    def test_remove_owner(self):
        new_sub = Subscribed("new sub", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        new_sub.un_appoint_owner(self.owner_sub, self.test_shop)
        assert self.test_shop not in new_sub.appointments.keys()
        try:
            new_shop = Shop(2)
            test_owner_2 = ShopOwner(new_shop)
            new_sub_2 = Subscribed("new sub 2", "0")
            new_sub_2.appointments[new_shop] = test_owner_2
            new_sub.appoint_owner(new_sub_2, new_shop)
            new_sub.un_appoint_owner(self.owner_sub, new_shop)
            assert False
        except Exception as e:
            pass

    def test_wrong_owner(self):
        new_sub = Subscribed("new sub", "0")
        new_sub2 = Subscribed("new sub", "0")
        app2 = ShopOwner(self.test_shop, self.owner_app)
        new_sub2.appointments[self.test_shop] = app2
        new_sub.appoint_manager(self.owner_sub, self.test_shop, [])
        try:
            new_sub.un_appoint_manager(new_sub2, self.test_shop, [])
            assert False
        except Exception as e:
            pass

    def test_cascade_owner_unappointment(self):
        new_sub = Subscribed("new sub", "0")
        new_sub2 = Subscribed("new sub", "0")
        new_sub3 = Subscribed("new sub", "0")
        new_sub.appoint_owner(self.owner_sub, self.test_shop)
        new_sub2.appoint_owner(new_sub, self.test_shop)
        new_sub3.appoint_owner(new_sub, self.test_shop)
        new_sub.un_appoint_owner(self.owner_sub, self.test_shop)
        assert self.test_shop not in new_sub3.appointments.keys()
