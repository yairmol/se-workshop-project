import unittest

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User


class ShoppingCartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.shop1 = Shop()
        self.shop2 = Shop()
        self.user = User()
        self.bamba = Product("bamba", 15, "bamba teima", 3)
        self.bisli = Product("bisli", 25, "bisli taim", 3)
        self.humus = Product("humus", 7, "humus taim", 3)

    # def clear(self):
    #     self.user.cart.remove_all_shopping_bags()
    #
    def add_product_to_cart1(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba)
        assert self.user.cart == {self.shop1: {self.bamba: 1}}

    def add_product_to_cart2(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bisli)
        self.user.save_product_to_cart(self.shop2, self.humus)
        assert self.user.cart == {self.shop1: {self.bamba: 1, self.bisli: 1}, self.shop2: {self.humus: 1}}

    def add_product_to_cart3(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bisli)
        self.user.save_product_to_cart(self.shop2, self.humus)
        assert self.user.cart == {self.shop1: {self.bamba: 3, self.bisli: 1}, self.shop2: {self.humus: 1}}

    def remove_bag_from_cart1(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bisli)
        self.user.save_product_to_cart(self.shop2, self.humus)
        self.user.cart.remove_shopping_bag(self.shop1)
        assert self.user.cart == {self.shop2: {self.humus: 1}}

    def remove_bag_from_cart2(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba)
        self.user.save_product_to_cart(self.shop1, self.bisli)
        self.user.save_product_to_cart(self.shop2, self.humus)
        self.user.cart.remove_shopping_bag(self.shop2)
        assert self.user.cart == {self.shop1: {self.bamba: 1, self.bisli: 1}}


if __name__ == '__main__':
    unittest.main()
