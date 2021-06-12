import unittest
from datetime import datetime
from unittest import TestCase

from data_model import ConditionsModel as Cm
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition, TimeWindowForCategoryCondition, \
    TimeWindowForProductCondition, DateWindowForCategoryCondition, DateWindowForProductCondition, ANDCondition, \
    ORCondition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.tests.mocks import DeliveryMock, PaymentMock
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.payment_module.payment_system import IPaymentsFacade

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
        IPaymentsFacade.get_payment_facade = lambda: PaymentMock(True)
        IDeliveryFacade.get_delivery_facade = lambda: DeliveryMock(True)
        self.shop = Shop(**shop1)
        self.bag = ShoppingBag(self.shop)
        self.products = [Product(**p) for p in products]
        self.product = self.products[0]

    def test_MaxQuantityForProductCondition(self):
        condition_dict = {Cm.MAX_QUANTITY: 5, Cm.PRODUCT: self.product.product_id}
        condition = MaxQuantityForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_TimeWindowForCategoryCondition(self):
        condition_dict = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:59', Cm.CATEGORY: "aaa"}
        condition = TimeWindowForCategoryCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_TimeWindowForProductCondition(self):
        condition_dict = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:59', Cm.PRODUCT: self.product.product_id}
        condition = TimeWindowForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_DateWindowForCategoryCondition(self):
        condition_dict = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '30/7/2021', Cm.CATEGORY: "aaa"}
        condition = DateWindowForCategoryCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_DateWindowForProductCondition(self):
        condition_dict = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '30/7/2021', Cm.PRODUCT: self.product.product_id}
        condition = DateWindowForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertTrue(self.bag.resolve_shop_conditions())

    def test_Fail_MaxQuantityForProductCondition(self):
        condition_dict = {Cm.MAX_QUANTITY: 3, Cm.PRODUCT: self.product.product_id}
        condition = MaxQuantityForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_TimeWindowForCategoryCondition(self):
        condition_dict = {Cm.MIN_TIME: '08:00', Cm.MAX_TIME: '9:00', Cm.CATEGORY: "aaa"}
        condition = TimeWindowForCategoryCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_TimeWindowForProductCondition(self):
        condition_dict = {Cm.MIN_TIME: '08:00', Cm.MAX_TIME: '9:00', Cm.PRODUCT: self.product.product_id}
        condition = TimeWindowForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_DateWindowForCategoryCondition(self):
        condition_dict = {Cm.MIN_DATE: '20/5/2022', Cm.MAX_DATE: '30/5/2022', Cm.CATEGORY: "aaa"}
        condition = DateWindowForCategoryCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())

    def test_Fail_DateWindowForProductCondition(self):
        condition_dict = {Cm.MIN_DATE: '20/5/2022', Cm.MAX_DATE: '30/5/2022', Cm.PRODUCT: self.product.product_id}
        condition = DateWindowForProductCondition(condition_dict)
        self.shop.add_purchase_condition(condition)
        amount = 4
        self.bag.add_product(self.product, amount)
        self.assertFalse(self.bag.resolve_shop_conditions())


    def test_all_conditions(self):
        condition_dict1 = {Cm.MAX_QUANTITY: 5, Cm.PRODUCT: self.product.product_id}
        condition1 = MaxQuantityForProductCondition(condition_dict1)
        condition_dict2 = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:00', Cm.CATEGORY: "aaa"}
        condition2 = TimeWindowForCategoryCondition(condition_dict2)
        condition_dict3 = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '23:00', Cm.PRODUCT: self.product.product_id}
        condition3 = TimeWindowForProductCondition(condition_dict3)
        condition_dict4 = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '30/7/2021', Cm.CATEGORY: "aaa"}
        condition4 = DateWindowForCategoryCondition(condition_dict4)
        condition_dict5 = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '30/7/2021', Cm.PRODUCT: self.product.product_id}
        condition5 = DateWindowForProductCondition(condition_dict5)
        condition_dict6 = {Cm.MAX_QUANTITY: 3, Cm.PRODUCT: self.product.product_id}
        condition6 = MaxQuantityForProductCondition(condition_dict6)
        condition_dict7 = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '00:01', Cm.CATEGORY: "aaa"}
        condition7 = TimeWindowForCategoryCondition(condition_dict7)
        condition_dict8 = {Cm.MIN_TIME: '00:00', Cm.MAX_TIME: '00:01', Cm.PRODUCT: self.product.product_id}
        condition8 = TimeWindowForProductCondition(condition_dict8)
        condition_dict9 = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '2/5/2021', Cm.CATEGORY: "aaa"}
        condition9 = DateWindowForCategoryCondition(condition_dict9)
        condition_dict10 = {Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '2/5/2021', Cm.PRODUCT: self.product.product_id}
        condition10 = DateWindowForProductCondition(condition_dict10)

        and_condition_dict = {Cm.CONDITIONS: [condition1, condition2, condition3, condition4, condition5]}
        or_condition_dict = {Cm.CONDITIONS: [condition6, condition7, condition8, condition9, condition10, condition5]}

        and_condition = ANDCondition(and_condition_dict)
        or_condition = ORCondition(or_condition_dict)

        self.shop.add_purchase_condition(condition1)
        self.shop.add_purchase_condition(condition2)
        self.shop.add_purchase_condition(condition3)
        self.shop.add_purchase_condition(condition4)
        self.shop.add_purchase_condition(condition5)
        self.shop.add_purchase_condition(and_condition)
        self.shop.add_purchase_condition(or_condition)

        self.bag.add_product(self.products[0], 4)
        self.bag.add_product(self.products[1], 4)
        self.bag.add_product(self.products[2], 1)
        self.bag.add_product(self.products[3], 10)
        self.assertTrue(self.bag.resolve_shop_conditions())


if __name__ == '__main__':
    unittest.main()
