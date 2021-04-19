import unittest

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User

shop_dict = {"shop_name": "s1", "description": "desc"}


class ShoppingCartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.shop1 = Shop(shop_dict)
        self.shop2 = Shop(shop_dict)
        self.user = User()
        self.bamba = Product("bamba", 15, "bamba teima", 3)
        self.bisli = Product("bisli", 25, "bisli taim", 3)
        self.humus = Product("humus", 7, "humus taim", 3)

    # def clear(self):
    #     self.user_sess.cart.remove_all_shopping_bags()
    #
    def test_add_product_to_cart1(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        assert self.user.cart.shopping_bags[self.shop1].products[self.bamba] == 1, "add product fail"

    def test_add_product_to_cart2(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 2)
        assert self.user.cart.shopping_bags[self.shop1].products[self.bamba] == 1, "add product fail"
        assert self.user.cart.shopping_bags[self.shop1].products[self.bisli] == 1, "add product fail"
        assert self.user.cart.shopping_bags[self.shop2].products[self.humus] == 2, "add product fail"

    def test_add_product_to_cart3(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bamba, 2)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 1)
        assert self.user.cart.shopping_bags[self.shop1].products[self.bamba] == 4, "add product fail"
        assert self.user.cart.shopping_bags[self.shop1].products[self.bisli] == 1, "add product fail"
        assert self.user.cart.shopping_bags[self.shop2].products[self.humus] == 1, "add product fail"

    def test_remove_bag_from_cart1(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 1)
        self.user.cart.remove_shopping_bag(self.shop1)
        assert len(self.user.cart.shopping_bags) == 1, "remove bag failed"
        assert self.user.cart.shopping_bags[self.shop2].products[self.humus] == 1, "add product fail"

    def test_remove_bag_from_cart2(self):
        # self.clear()
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 1)
        self.user.cart.remove_shopping_bag(self.shop2)
        assert len(self.user.cart.shopping_bags) == 1, "remove bag failed"
        assert self.user.cart.shopping_bags[self.shop1].products[self.bamba] == 1, "add product fail"
        assert self.user.cart.shopping_bags[self.shop1].products[self.bisli] == 1, "add product fail"


if __name__ == '__main__':
    unittest.main()
