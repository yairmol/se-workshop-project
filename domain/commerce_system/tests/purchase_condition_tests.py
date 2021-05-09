import unittest
from datetime import datetime, time
from unittest import TestCase

from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition, TimeWindowForCategoryCondition, \
    TimeWindowForProductCondition, DateWindowForCategoryCondition, DateWindowForProductCondition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.tests.mocks import DeliveryMock, PaymentMock

shop1 = {"shop_name": "s1", "description": "a shop1"}
prices = [5, 2.8, 3, 90]
products = [
    {"product_name": "p1", "description": "a prod", "price": prices[0], "quantity": 10, "categories": ["aaa", "bbb"]},
    {"product_name": "p2", "description": "a prod 2", "price": prices[1], "quantity": 7, "categories": ["aaa", "ccc"]},
    {"product_name": "p3", "description": "a prod 3", "price": prices[2], "quantity": 2, "categories": ["aaa", "ddd"]},
    {"product_name": "p4", "description": "a prod 4", "price": prices[3], "quantity": 30, "categories": ["aaa", "eee"]},
]
amounts = [4, 2, 7, 5]
payment_details = {
    "credit_card_number": "4580-0000-1111-2222", "cvv": "012", "expiration_date": datetime(2024, 6, 1).timestamp()
}
# condition1 = MaxQuantityForProductCondition(5,)
# condition2 = MaxTimeForCategoryCondition()

assert len(products) == len(amounts) == len(prices), "data lengths must be equal"


class PurchaseConditionTests(TestCase):
    def setUp(self) -> None:
        self.shop = Shop(**shop1)
        self.bag = ShoppingBag(self.shop)
        self.products = [Product(**p) for p in products]
        self.product = self.products[0]

    def test_MaxQuantityForProductCondition(self):
        condition = MaxQuantityForProductCondition(5, self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_TimeWindowForCategoryCondition(self):
        condition = TimeWindowForCategoryCondition(time(0, 0), time(23, 0), category="aaa")
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_TimeWindowForProductCondition(self):
        condition = TimeWindowForProductCondition(time(0, 0), time(23, 0), self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_DateWindowForCategoryCondition(self):
        condition = DateWindowForCategoryCondition(datetime(year=2021, month=5, day=1),
                                                   datetime(year=2021, month=5, day=30), category="aaa")
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_DateWindowForProductCondition(self):
        condition = DateWindowForProductCondition(datetime(year=2021, month=5, day=1),
                                                  datetime(year=2021, month=5, day=30), self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_Fail_MaxQuantityForProductCondition(self):
        condition = MaxQuantityForProductCondition(3, self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_TimeWindowForCategoryCondition(self):
        condition = TimeWindowForCategoryCondition(time(8, 0), time(23, 0), category="aaa")
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_TimeWindowForProductCondition(self):
        condition = TimeWindowForProductCondition(time(8, 0), time(23, 0), self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_DateWindowForCategoryCondition(self):
        condition = DateWindowForCategoryCondition(datetime(year=2021, month=5, day=20),
                                                   datetime(year=2021, month=5, day=30), category="aaa")
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_DateWindowForProductCondition(self):
        condition = DateWindowForProductCondition(datetime(year=2021, month=5, day=20),
                                                  datetime(year=2021, month=5, day=30), self.product)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_all_conditions(self):
        condition1 = MaxQuantityForProductCondition(5, self.product)
        condition2 = MaxQuantityForProductCondition(5, self.products[1])
        condition3 = MaxQuantityForProductCondition(5, self.products[2])
        condition4 = MaxQuantityForProductCondition(10, self.products[3])
        condition5 = TimeWindowForCategoryCondition(time(0, 0), time(23, 0), category="aaa")
        condition6 = TimeWindowForProductCondition(time(0, 0), time(23, 0), self.products[1])
        condition7 = DateWindowForCategoryCondition(datetime(year=2021, month=5, day=1),
                                                    datetime(year=2021, month=5, day=30), category="aaa")
        condition8 = DateWindowForCategoryCondition(datetime(year=2021, month=5, day=1),
                                                    datetime(year=2021, month=5, day=30), self.products[2])
        self.shop.add_purchase_condition(condition1)
        self.shop.add_purchase_condition(condition2)
        self.shop.add_purchase_condition(condition3)
        self.shop.add_purchase_condition(condition4)
        self.shop.add_purchase_condition(condition5)
        self.shop.add_purchase_condition(condition6)
        self.shop.add_purchase_condition(condition7)
        self.shop.add_purchase_condition(condition8)
        self.bag.add_product(self.products[0], 4)
        self.bag.add_product(self.products[1], 4)
        self.bag.add_product(self.products[2], 1)
        self.bag.add_product(self.products[3], 10)
        self.assertTrue(self.bag.resolve_shop_conditions())




if __name__ == '__main__':
    unittest.main()
