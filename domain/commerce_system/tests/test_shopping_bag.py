import unittest
from datetime import datetime
from unittest import TestCase

from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition, DateWindowForCategoryCondition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.tests.mocks import DeliveryMock, PaymentMock

shop1 = {"shop_name": "s1", "description": "a shop1"}
prices = [5, 2.8, 3, 90]
products = [
    {"product_name": "p1", "description": "a prod", "price": prices[0], "quantity": 10},
    {"product_name": "p2", "description": "a prod 2", "price": prices[1], "quantity": 7},
    {"product_name": "p3", "description": "a prod 3", "price": prices[2], "quantity": 2},
    {"product_name": "p4", "description": "a prod 4", "price": prices[3], "quantity": 30},
]
amounts = [4, 2, 7, 5]
payment_details = {
    "credit_card_number": "4580-0000-1111-2222", "cvv": "012", "expiration_date": datetime(2024, 6, 1).timestamp()
}
delivery_details = {}
username = "aviv"

assert len(products) == len(amounts) == len(prices), "data lengths must be equal"


class BagTests(TestCase):
    def setUp(self) -> None:
        self.shop = Shop(**shop1)
        self.bag = ShoppingBag(self.shop)
        self.products = [Product(**p) for p in products]
        self.product = self.products[0]

    def test_add_product(self):
        amount = 5
        self.bag.add_product(self.product, amount)
        self.assertEquals(list(self.bag.products.items()), [(self.product, amount)])

    def test_update_quantity(self):
        init_amount = 5
        additional_amount = 4
        self.bag.add_product(self.product, init_amount)
        self.bag.add_product(self.product, additional_amount)
        self.assertEquals(list(self.bag.products.items()), [(self.product, init_amount + additional_amount)])

    def test_update_remove_some_quantity(self):
        init_amount = 5
        remove_amount = 4
        self.bag.add_product(self.product, init_amount)
        self.bag.remove_product(self.product, remove_amount)
        self.assertEquals(list(self.bag.products.items()), [(self.product, init_amount - remove_amount)])

    def test_remove_product(self):
        init_amount = 5
        self.bag.add_product(self.product, init_amount)
        self.bag.remove_product(self.product, init_amount)
        self.assertEquals(list(self.bag.products.items()), [])

    def test_calculate_price(self):
        # no purchase policies or discounts
        init_amount = 5
        self.bag.add_product(self.product, init_amount)
        self.assertEquals(self.bag.calculate_price(), self.product.price * init_amount)

    def test_calculate_price_several_products(self):
        [self.bag.add_product(p, a) for p, a in zip(self.products, amounts)]
        expected = sum([p.price * a for p, a in zip(self.products, amounts)])
        self.assertEquals(self.bag.calculate_price(), expected)

    def test_purchase_bag_payment_and_delivery_success(self):
        amount_idx = 0
        amount_to_buy = amounts[amount_idx]
        self.bag.payment_facade = PaymentMock(True)
        self.bag.delivery_facade = DeliveryMock(True)
        self.bag.add_product(self.product, amount_to_buy)
        product_quantity = self.product.get_quantity()
        transaction = self.bag.purchase_bag(username, payment_details, delivery_details)
        self.assertNotEqual(transaction, None)
        self.assertEquals(self.bag.products, {})
        self.assertEquals(transaction.price, amount_to_buy * self.product.price)
        self.assertEquals(transaction.shop, self.shop)
        self.assertEquals(list(transaction.products), [ProductDTO(self.product, amount_to_buy)])
        self.assertEquals(self.product.get_quantity(), product_quantity - amount_to_buy)

    def test_purchase_bag_payment_and_delivery_with_condition_success(self):
        amount_idx = 0
        amount_to_buy = amounts[amount_idx]
        self.bag.payment_facade = PaymentMock(True)
        self.bag.delivery_facade = DeliveryMock(True)
        self.bag.add_product(self.product, amount_to_buy)
        product_quantity = self.product.get_quantity()
        condition_dict = {"max_quantity": amount_to_buy + 1, "product": self.product.product_id}
        condition = MaxQuantityForProductCondition(condition_dict)
        self.bag.shop.add_purchase_condition(condition)
        transaction = self.bag.purchase_bag(username, payment_details, delivery_details)
        self.assertNotEqual(transaction, None)
        self.assertEquals(self.bag.products, {})
        self.assertEquals(transaction.price, amount_to_buy * self.product.price)
        self.assertEquals(transaction.shop, self.shop)
        self.assertEquals(list(transaction.products), [ProductDTO(self.product, amount_to_buy)])
        self.assertEquals(self.product.get_quantity(), product_quantity - amount_to_buy)

    def test_purchase_bag_payment_works_delivery_fails(self):
        amount_idx = 0
        amount = amounts[amount_idx]
        pay_facade, deliver_facade = PaymentMock(True), DeliveryMock(True)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        self.bag.add_product(self.product, amount)
        product_quantity = self.product.get_quantity()
        products_copy = self.bag.products.copy()
        condition_dict = {"max_quantity": amount - 1, "product": self.product.product_id}
        condition = MaxQuantityForProductCondition(condition_dict)
        self.bag.shop.add_purchase_condition(condition)
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(not pay_facade.pay_called or (pay_facade.pay_called and pay_facade.pay_cancelled))
        self.assertTrue(self.product.get_quantity(), product_quantity)

    def test_purchase_bag_with_condition_fails(self):
        amount_idx = 0
        amount = amounts[amount_idx]
        pay_facade, deliver_facade = PaymentMock(True), DeliveryMock(False)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        self.bag.add_product(self.product, amount)
        product_quantity = self.product.get_quantity()
        products_copy = self.bag.products.copy()
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(not pay_facade.pay_called or (pay_facade.pay_called and pay_facade.pay_cancelled))
        self.assertTrue(deliver_facade.delivery_called)
        self.assertTrue(self.product.get_quantity(), product_quantity)

    def test_purchase_bag_payment_fails_delivery_works(self):
        amount_idx = 0
        amount = amounts[amount_idx]
        pay_facade, deliver_facade = PaymentMock(False), DeliveryMock(True)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        self.bag.add_product(self.product, amount)
        product_quantity = self.product.get_quantity()
        products_copy = self.bag.products.copy()
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(
            not deliver_facade.delivery_called
            or (deliver_facade.delivery_called and deliver_facade.delivery_cancelled)
        )
        self.assertTrue(pay_facade.pay_called)
        self.assertTrue(self.product.get_quantity(), product_quantity)

    def test_purchase_bag_payment_and_delivery_works_amount_to_big(self):
        amount = self.product.get_quantity() + 1
        pay_facade, deliver_facade = PaymentMock(True), DeliveryMock(True)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        self.bag.add_product(self.product, amount)
        product_quantity = self.product.get_quantity()
        products_copy = self.bag.products.copy()
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(
            not deliver_facade.delivery_called
            or (deliver_facade.delivery_called and deliver_facade.delivery_cancelled)
        )
        self.assertTrue(not pay_facade.pay_called or (pay_facade.pay_called and pay_facade.pay_cancelled))
        self.assertTrue(self.product.get_quantity(), product_quantity)

    def test_purchase_bag_payment_and_delivery_works_date_condition_fails(self):
        amount = self.product.get_quantity() + 1
        pay_facade, deliver_facade = PaymentMock(True), DeliveryMock(True)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        self.bag.add_product(self.product, amount)
        product_quantity = self.product.get_quantity()
        self.product.categories += ["c1"]
        products_copy = self.bag.products.copy()
        condition_dict = {
            "min_date": '1/5/2021',
            "max_date": '2/5/2021',
            "category": "c1"
        }
        condition = DateWindowForCategoryCondition(condition_dict)
        self.bag.shop.add_purchase_condition(condition)
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(
            not deliver_facade.delivery_called
            or (deliver_facade.delivery_called and deliver_facade.delivery_cancelled)
        )
        self.assertTrue(not pay_facade.pay_called or (pay_facade.pay_called and pay_facade.pay_cancelled))
        self.assertTrue(self.product.get_quantity(), product_quantity)

    def test_purchase_bag_several_products_to_big_amount(self):
        amounts_copy = amounts.copy()
        pay_facade, deliver_facade = PaymentMock(True), DeliveryMock(True)
        self.bag.payment_facade = pay_facade
        self.bag.delivery_facade = deliver_facade
        product_big_amount_idx = len(amounts_copy) - 1
        amounts_copy[product_big_amount_idx] = self.products[product_big_amount_idx].get_quantity() + 1
        [self.bag.add_product(p, a) for p, a in zip(self.products, amounts_copy)]
        product_quantities = [p.get_quantity() for p in self.products]
        products_copy = self.bag.products.copy()
        self.assertRaises(AssertionError, self.bag.purchase_bag, username, payment_details, delivery_details)
        self.assertEquals(self.bag.products, products_copy)
        self.assertTrue(
            not deliver_facade.delivery_called
            or (deliver_facade.delivery_called and deliver_facade.delivery_cancelled)
        )
        self.assertTrue(not pay_facade.pay_called or (pay_facade.pay_called and pay_facade.pay_cancelled))
        self.assertTrue([p.get_quantity() for p in self.products], product_quantities)


if __name__ == "__main__":
    unittest.main()
