import unittest
import threading as th
from domain.commerce_system.appointment import ShopOwner
from domain.commerce_system.shop import Shop

shop_dict = {"shop_name": "s1", "description": "desc"}
tost = {"product_name": "tost", "price": 115, "description": "tost taim", "quantity": 3}
tost2 = {"product_name": "tost2", "price": 116, "description": "tost2 taim", "quantity": 4}


def run_parallel_test(f1, f2):
    t1, t2 = th.Thread(target=f1), th.Thread(target=f2)
    t1.start(), t2.start()
    t1.join(), t2.join()


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.shop = Shop(**shop_dict)
        self.bamba = {"product_name": "eeee", "price": 5, "description": "bamba teima", "quantity": 3}
        self.bisli = {"product_name": "bisli", "price": 25, "description": "bisli taim", "quantity": 3}
        self.humus = {"product_name": "humus", "price": 7, "description": "humus taim", "quantity": 3}
        self.shop.add_product(**self.bamba)
        self.shop.add_product(**self.bisli)
        self.shop.add_product(**self.humus)
        self.shop_owner = ShopOwner(self.shop)

    def test_add_product(self):
        self.shop_owner.add_product(**tost)
        self.shop_owner.add_product(**tost2)
        assert self.shop.has_product("tost") and self.shop.has_product("tost2")

    def test_add_product_parallel(self):
        def add1(x):
            return lambda: x.shop_owner.add_product(**tost)

        def add2(x):
            return lambda: x.shop_owner.add_product(**tost2)

        run_parallel_test(add1(self), add2(self))
        assert self.shop.has_product("tost") and self.shop.has_product("tost2")

    def test_delete_product(self):
        self.shop.add_product(**tost)
        self.shop.add_product(**tost2)
        tost_id = self.shop.get_id("tost")
        tost2_id = self.shop.get_id("tost2")
        self.shop_owner.delete_product(tost_id)
        self.shop_owner.delete_product(tost2_id)
        assert not self.shop.has_product("tost") and not self.shop.has_product("tost2")

    def test_delete_product_parallel(self):
        self.shop.add_product(**tost)
        self.shop.add_product(**tost2)

        def del1(x):
            def a():
                tost_id = x.shop.get_id("tost")
                x.shop_owner.delete_product(tost_id)
            return a

        def del2(x):
            def a():
                tost_id = x.shop.get_id("tost2")
                x.shop_owner.delete_product(tost_id)
            return a

        run_parallel_test(del1(self), del2(self))
        assert not self.shop.has_product("tost") and not self.shop.has_product("tost2")

    def test_edit_product(self):
        tost_dup = tost.copy()
        tost_dup["quantity"] = 12
        tost2_dup = tost2.copy()
        tost2_dup["quantity"] = 54
        self.shop.add_product(**tost_dup)
        self.shop.add_product(**tost2_dup)
        tost_id = self.shop.get_id("tost")
        tost2_id = self.shop.get_id("tost2")
        self.shop_owner.edit_product(tost_id, product_name="tost3")
        self.shop_owner.edit_product(tost2_id, product_name="tost4")
        self.assertFalse(self.shop.has_product("tost"))
        self.assertFalse(self.shop.has_product("tost2"))
        self.assertTrue(self.shop.has_product("tost3"))
        self.assertTrue(self.shop.has_product("tost4"))
