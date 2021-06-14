import unittest

from domain.commerce_system.product import Product, BuyNow
from domain.discount_module.discount_calculator import *

product_dict1 = {"product_name": "Armani shirt", "price": 299.9, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product_dict2 = {"product_name": "Armani Belt", "price": 99.9, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
p1 = Product(**product_dict1)
p2 = Product(**product_dict2)


class ConditionTests(unittest.TestCase):

    # def setUp(self):

    # Min Quantity Tests ---------------------------------------------------------
    def test_product_quantity_condition1(self):
        simple_condition = ProductQuantityCondition(3, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 3, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}

        assert simple_condition.resolve(products)

    def test_product_quantity_condition2(self):
        simple_condition = ProductQuantityCondition(3, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}

        assert not simple_condition.resolve(products)

    def test_product_quantity_condition3(self):
        simple_condition = ProductQuantityCondition(0, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_quantity_condition1(self):
        simple_condition = CategoryQuantityCondition(3, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_quantity_condition2(self):
        simple_condition = CategoryQuantityCondition(0, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 0, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_quantity_condition3(self):
        simple_condition = CategoryQuantityCondition(10, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 5, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_quantity_condition4(self):
        simple_condition = CategoryQuantityCondition(10, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 4, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert not simple_condition.resolve(products)

    # Min Sum Tests ---------------------------------------------------------
    def test_Total_Sum_condition1(self):
        simple_condition = TotalSumCondition(200)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 5, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Total_Sum_condition2(self):
        simple_condition = TotalSumCondition(100)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert not simple_condition.resolve(products)

    def test_Total_Sum_condition3(self):
        simple_condition = TotalSumCondition(299)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 0, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_Sum_condition1(self):
        simple_condition = CategorySumCondition(100, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_Sum_condition2(self):
        simple_condition = CategorySumCondition(500, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert not simple_condition.resolve(products)

    def test_Category_Sum_condition3(self):
        simple_condition = CategorySumCondition(0, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 0, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_Sum_condition4(self):
        simple_condition = CategorySumCondition(100, 'dokrim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 0, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_Sum_condition5(self):
        simple_condition = CategorySumCondition(100, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type)}
        assert simple_condition.resolve(products)

    def test_Category_Sum_condition6(self):
        simple_condition = CategorySumCondition(100, 'gvarim')
        products = {}
        assert not simple_condition.resolve(products)

    # Multiple conditions tests ---------------------------------------------------------
    
    # AND Condition Tests 
    def test_ANDCondition1(self):
        simple_condition1 = CategorySumCondition(100, 'gvarim')
        simple_condition2 = CategorySumCondition(100, 'dokrim')
        cond_lst = [simple_condition1, simple_condition2]
        and_condition = ANDCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert and_condition.resolve(products)

    def test_ANDCondition2(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(100, 'dokrim')
        cond_lst = [simple_condition1, simple_condition2]
        and_condition = ANDCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert and_condition.resolve(products)

    def test_ANDCondition3(self):
        cond_lst = []
        and_condition = ANDCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}
        assert and_condition.resolve(products)

    def test_ANDCondition4(self):
        simple_condition1 = ProductQuantityCondition(100, p1.product_id)
        simple_condition2 = CategorySumCondition(100, 'gvarim')
        cond_lst = [simple_condition1, simple_condition2]
        and_condition = ANDCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert not and_condition.resolve(products)

    def test_ANDCondition5(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(10000, 'gvarim')
        cond_lst = [simple_condition1, simple_condition2]
        and_condition = ANDCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 2, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert not and_condition.resolve(products)

    # OR ConditionTests = Returns true if at least 1 condition is met
    def test_OR_Condition1(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(200, 'gvarim')
        cond_lst = [simple_condition1, simple_condition2]
        or_condition = ORCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert or_condition.resolve(products)

    def test_OR_Condition2(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(20000, 'gvarim')
        cond_lst = [simple_condition1, simple_condition2]
        or_condition = ORCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert or_condition.resolve(products)

    def test_OR_Condition3(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(20000, 'gvarim')
        cond_lst = [simple_condition1, simple_condition2]
        or_condition = ORCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert not or_condition.resolve(products)

    def test_OR_Condition4(self):
        cond_lst = []
        or_condition = ORCondition(cond_lst)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 0, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert not or_condition.resolve(products)

    def test_AND_Composed_of_OR_Condiion(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(20000, 'dokrim')
        cond_lst1 = [simple_condition1, simple_condition2]
        or_condition = ORCondition(cond_lst1)

        simple_condition1 = ProductQuantityCondition(1, p2.product_id)
        simple_condition2 = CategorySumCondition(100, 'gvarim')
        cond_lst2 = [simple_condition1, simple_condition2]
        or_condition2 = ORCondition(cond_lst2)

        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        and_condition = ANDCondition([or_condition,or_condition2])
        assert and_condition.resolve(products)

    def test_OR_Composed_of_AND_Condiion(self):
        simple_condition1 = ProductQuantityCondition(1, p1.product_id)
        simple_condition2 = CategorySumCondition(100, 'gvarim')
        cond_lst1 = [simple_condition1, simple_condition2]
        and_condition = ANDCondition(cond_lst1)

        simple_condition1 = ProductQuantityCondition(100, p2.product_id)
        simple_condition2 = CategorySumCondition(10000, 'gvarim')
        cond_lst2 = [simple_condition1, simple_condition2]
        and_condition2 = ANDCondition(cond_lst2)

        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 5, purchase_type)}
        assert and_condition.resolve(products)