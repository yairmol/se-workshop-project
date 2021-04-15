import unittest
from unittest.mock import MagicMock

from domain.commerce_system.appointment_state import ShopOwner, ShopManager
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.subscribed import Subscribed


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.owner_sub = Subscribed("test sub")
        self.test_shop = Shop(1)
        self.owner_app = ShopOwner(self.test_shop)
        self.owner_sub.appointments[self.test_shop] = self.owner_app

    def test_add_appointment(self):
        new_sub = Subscribed("new sub")
        app = ShopManager(self.test_shop)
        new_sub.add_appointment(self.owner_sub, self.test_shop, app)
        assert (self.test_shop, app) in new_sub.appointments.items()
        try:
            new_shop = Shop(2)
            new_sub.add_appointment(self.owner_sub, self.test_shop, app)
            assert False
        except Exception as e:
            pass

    def test_remove_appointment(self):
        new_sub = Subscribed("new sub")
        app = ShopManager(self.test_shop)
        new_sub.appointments[self.test_shop] = app
        new_sub.remove_appointment(self.owner_sub, self.test_shop)
        assert (self.test_shop, app) not in new_sub.appointments.items()
        try:
            new_shop = Shop(2)
            new_sub.appointments[new_shop] = app
            new_sub.remove_appointment(self.owner_sub, new_shop)
            assert False
        except Exception as e:
            pass
