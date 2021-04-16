import unittest
from unittest.mock import MagicMock

from domain.commerce_system.appointment import ShopOwner
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.shop = Shop(1)
        self.bamba = Product("bamba", 15, "bamba teima", 3)
        self.bisli = Product("bisli", 25, "bisli taim", 3)
        self.humus = Product("humus", 7, "humus taim", 3)
        self.shop.add_product(self.bamba)
        self.shop.add_product(self.bisli)
        self.shop.add_product(self.humus)
        self.shop_owner = ShopOwner()

    def test_add_product(self):
        tost = Product("tost", 115, "tost taim", 3)
        tost2 = Product("tost2", 116, "tost2 taim", 3)
        self.shop_owner.add_product(self.shop, tost)
        self.shop_owner.add_product(self.shop, tost2)
        assert self.shop.has_product("tost") and self.shop.has_product("tost2")

    def test_delete_product(self):
        tost = Product("tost", 115, "tost taim", 3)
        tost2 = Product("tost2", 116, "tost2 taim", 5)
        self.shop.add_product(tost)
        self.shop.add_product(tost2)
        tost_id = self.shop.get_id("tost")
        tost2_id = self.shop.get_id("tost2")
        self.shop_owner.delete_product(self.shop, tost_id)
        self.shop_owner.delete_product(self.shop, tost2_id)
        assert not self.shop.has_product("tost") and not self.shop.has_product("tost2")

    def test_edit_product(self):
        tost = Product("tost", 115, "tost taim")
        tost2 = Product("tost2", 116, "tost2 taim")
        self.shop.add_product(tost, 2)
        self.shop.add_product(tost2, 3)
        tost_id = self.shop.get_id("tost")
        tost2_id = self.shop.get_id("tost2")
        self.shop_owner.edit_product(self.shop, tost_id, name="tost3")
        self.shop_owner.edit_product(self.shop, tost2_id, name="tost4")
        assert not self.shop.has_product("tost") and not self.shop.has_product("tost2") and self.shop.has_product("tost3") and self.shop.has_product("tost4")
