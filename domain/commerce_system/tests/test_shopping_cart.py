import unittest
import threading as th
from datetime import datetime
from typing import List, Dict

from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.tests.mocks import PaymentMock, DeliveryMock
from domain.commerce_system.user import User
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.payment_module.payment_system import IPaymentsFacade

shops = [
    {"shop_name": "s1", "description": "desc"},
    {"shop_name": "s2", "description": "desc"},
    {"shop_name": "s3", "description": "yet another shop"},
]
product_keys = ["product_name", "price", "description", "quantity"]
products = [
    dict(zip(product_keys, ["bamba", 15, "bamba teima", 3])),
    dict(zip(product_keys, ["bisli", 25, "bisli taim", 3])),
    dict(zip(product_keys, ["humus", 7, "humus taim", 3])),
    dict(zip(product_keys, ["baygale", 8, "baygale yavesh", 4]))
]
payment_details = {
    "credit_card_number": "4580-0000-1111-2222", "cvv": "012", "expiration_date": datetime(2024, 6, 1).timestamp()
}
delivery_details = {}

username = "aviv"


def run_parallel_test(f1, f2):
    t1, t2 = th.Thread(target=f1), th.Thread(target=f2)
    t1.start(), t2.start()
    t1.join(), t2.join()


class ShoppingCartTests(unittest.TestCase):
    def setUp(self) -> None:
        IPaymentsFacade.get_payment_facade = lambda: PaymentMock(True)
        IDeliveryFacade.get_delivery_facade = lambda: DeliveryMock(True)
        self.shop1 = Shop(**shops[0])
        self.shop2 = Shop(**shops[1])
        self.shop3 = Shop(**shops[2])
        self.user = User()
        self.bamba = self.shop1.add_product(**products[0])
        self.bisli = self.shop1.add_product(**products[1])
        self.humus = self.shop2.add_product(**products[2])
        self.baygale = self.shop3.add_product(**products[3])
        self.products = [self.bamba, self.bisli, self.humus, self.baygale]

    def test_add_product_to_cart1(self):
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bamba].amount == 1)

    def test_add_product_to_cart2(self):
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 2)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bamba].amount == 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bisli].amount == 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop2].products[self.humus].amount == 2)

    def test_add_product_to_cart3(self):
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bamba, 1)
        self.user.save_product_to_cart(self.shop1, self.bamba, 2)
        self.user.save_product_to_cart(self.shop1, self.bisli, 1)
        self.user.save_product_to_cart(self.shop2, self.humus, 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bamba].amount == 4)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bisli].amount == 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop2].products[self.humus].amount == 1)

    def save_to_cart(self):
        amounts_bought = {
            self.bamba: 1,
            self.bisli: 1,
            self.humus: 1,
            self.baygale: 1,
        }
        self.user.save_product_to_cart(self.shop1, self.bamba, amounts_bought[self.bamba])
        self.user.save_product_to_cart(self.shop1, self.bisli, amounts_bought[self.baygale])
        self.user.save_product_to_cart(self.shop2, self.humus, amounts_bought[self.humus])
        self.user.save_product_to_cart(self.shop3, self.baygale, amounts_bought[self.baygale])
        return amounts_bought

    def test_remove_bag_from_cart1(self):
        self.save_to_cart()
        self.user.cart.remove_shopping_bag(self.shop1)
        self.assertTrue(len(self.user.cart.shopping_bags) == 2)
        self.assertTrue(self.user.cart.shopping_bags[self.shop2].products[self.humus].amount == 1)

    def test_remove_bag_from_cart2(self):
        self.save_to_cart()
        self.user.cart.remove_shopping_bag(self.shop2)
        self.assertTrue(len(self.user.cart.shopping_bags) == 2)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bamba] == 1)
        self.assertTrue(self.user.cart.shopping_bags[self.shop1].products[self.bisli] == 1)

    def test_remove_bag_from_cart_parallel(self):
        self.save_to_cart()

        def remove1(x):
            return lambda: x.user.cart.remove_shopping_bag(self.shop1)

        def remove2(x):
            return lambda: x.user.cart.remove_shopping_bag(self.shop2)

        run_parallel_test(remove1(self), remove2(self))
        self.assertTrue(len(self.user.cart.shopping_bags) == 1)

    def check_bags(self, bags: List[ShoppingBag]):
        for bag in bags:
            self.assertEqual(bag.products, {})
            self.assertTrue(bag.delivery_facade.delivery_called and not bag.delivery_facade.delivery_cancelled)
            self.assertTrue(bag.payment_facade.pay_called and not bag.payment_facade.pay_cancelled)

    def check_updated_quantities(
            self, previous_quantities: Dict[Product, int],
            amounts_bought: Dict[Product, int]
    ):
        for product in self.products:
            self.assertEqual(
                product.get_quantity(),
                previous_quantities[product] - amounts_bought[product]
            )

    def init_bags_facades(self):
        for bag in self.user.cart.shopping_bags.values():
            bag.payment_facade, bag.delivery_facade = PaymentMock(True), DeliveryMock(True)

    def init_purchase_data(self):
        ret = self.save_to_cart()
        self.init_bags_facades()
        return ret

    def test_purchase_cart_all(self):
        amounts_bought = self.init_purchase_data()
        quantities = {p: p.get_quantity() for p in self.products}
        bags = list(self.user.cart.shopping_bags.values())
        transactions = self.user.cart.purchase_cart(username, payment_details, delivery_details)
        self.assertEqual(len(transactions), len(bags))
        self.assertEqual(self.user.cart.shopping_bags, {})
        self.check_bags(bags)
        self.check_updated_quantities(quantities, amounts_bought)

    def check_purchase_failure(self):
        quantities = {p: p.get_quantity() for p in self.products}
        bags = self.user.cart.shopping_bags.copy()
        bags_products = {shop: bag.products.copy() for shop, bag in bags.items()}
        self.assertRaises(AssertionError, self.user.cart.purchase_cart, username, payment_details, delivery_details)
        # check that products quantities weren't changed
        amounts_bought = dict(zip(self.products, [0] * len(products)))
        self.check_updated_quantities(quantities, amounts_bought)
        # check bags are unchanged
        self.assertEqual(len(bags), len(self.user.cart.shopping_bags))
        for shop, bag in bags.items():
            self.assertEqual(self.user.cart.shopping_bags[shop].products, bags_products[shop])

    def test_purchase_cart_fails_in_the_middle_due_to_payment(self):
        self.init_purchase_data()
        self.user.cart.shopping_bags[self.shop3].payment_facade = PaymentMock(False)
        self.check_purchase_failure()

    def test_purchase_cart_fails_in_the_middle_due_to_payment_parallel(self):
        def f(x):
            return lambda: x.test_purchase_cart_fails_in_the_middle_due_to_payment()
        run_parallel_test(f(self), f(self))

    def test_purchase_cart_fails_in_the_middle_due_to_delivery(self):
        self.init_purchase_data()
        self.user.cart.shopping_bags[self.shop2].delivery_facade = DeliveryMock(False)
        self.check_purchase_failure()

    def test_purchase_cart_fails_in_the_middle_due_to_stock(self):
        self.init_purchase_data()
        self.user.cart.add_product(self.baygale, self.shop3, 100)
        self.check_purchase_failure()

    def test_purchase_cart_fails_in_the_middle_due_to_condition(self):
        self.init_purchase_data()
        condition_dict = {"max_quantity": 0, "product": self.bamba.product_id}
        condition = MaxQuantityForProductCondition(condition_dict)
        self.shop1.add_purchase_condition(condition)
        self.check_purchase_failure()

    def test_purchase_cart_what_you_can(self):
        amounts_bought = self.init_purchase_data()
        shop_fails = self.shop2
        self.user.cart.shopping_bags[shop_fails].delivery_facade = DeliveryMock(False)
        for p in amounts_bought.keys():
            if p in shop_fails.products.values():
                amounts_bought[p] = 0
        quantities = {p: p.get_quantity() for p in self.products}
        bags = self.user.cart.shopping_bags.copy()
        bag_fails = bags.pop(shop_fails)
        bag_fails_products = bag_fails.products.copy()
        transactions = self.user.cart.purchase_cart(username, payment_details, delivery_details, do_what_you_can=True)
        # check that products quantities were changed except from the one in shop_fails
        self.check_updated_quantities(quantities, amounts_bought)
        self.assertEqual(len(self.user.cart.shopping_bags), 1)
        # check that the shopping bags are emptied except for bag_fails
        self.check_bags(bags.values())
        self.assertEqual(self.user.cart.shopping_bags[shop_fails].products, bag_fails_products)
        # check that the number of successful transactions is correct
        self.assertEqual(len(bags), len(list(filter(lambda x: x is not None, transactions))))


if __name__ == '__main__':
    unittest.main()
