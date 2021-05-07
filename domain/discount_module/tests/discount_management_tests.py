import unittest

from domain.discount_module.discount_calculator import *
from domain.discount_module.discount_management import *

product_dict1 = {"product_name": "Armani shirt", "price": 300, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product_dict2 = {"product_name": "Armani Belt", "price": 100, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
p1 = Product(**product_dict1)
p2 = Product(**product_dict2)


class DiscountManagementTests(unittest.TestCase):
    # class SimpleCond(TypedDict):
    #     condition: str  # condition:( 'quantity / 'sum' )
    #     type: str  # ''' type:( 'product' / 'category' / 'shop') '''
    #     identifier: Union[int, str]  # identifier:( <product_id>/ <category_name>/'shop')
    #     num: int  # num: (<quantity> / <sum>)
    #
    # class DiscountDict(TypedDict):
    #     type: str  # ''' type:( 'product' / 'category' / 'shop') '''
    #     identifier: Union[int, str]  # identifier:( <product_id>/ <category_name>/'shop')
    #     percentage: int

    def setUp(self) -> None:
        self.simple_cond1: SimpleCond = {'condition': 'quantity', 'type': 'product', 'identifier': p1.product_id,
                                         'num': 1}
        self.simple_cond2: SimpleCond = {'condition': 'sum', 'type': 'shop', 'identifier': 'shop',
                                         'num': 50}

        self.simple_cond3: SimpleCond = {'condition': 'sum', 'type': 'shop', 'identifier': 'shop',
                                         'num': 1000000}  # failing simple cond

        self.And_cond1 = ['and', self.simple_cond1, self.simple_cond2]
        self.Or_cond1 = ['or', self.simple_cond1, self.simple_cond2]

        self.product1_discount_dict1: DiscountDict = {'type': 'product', 'identifier': p1.product_id, 'percentage': 20}
        self.product1_discount1 = ProductDiscount(False, None, 20, p1.product_id)

        self.product1_discount_dict2: DiscountDict = {'type': 'product', 'identifier': p1.product_id, 'percentage': 10}
        self.product1_discount2 = ProductDiscount(False, None, 10, p1.product_id)

    # condition: [str or SimpleCond or []]
    ''' Create Cond From simple cond Dict Tests --------------------------------------------------- '''
    def test_create_cond_from_simple_cond(self):
        cond_data = [self.simple_cond1]
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_And_cond(self):
        cond: Condition = DiscountManagement.create_cond(self.And_cond1)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_And_cond2(self):
        cond: Condition = DiscountManagement.create_cond(self.And_cond1)
        products = {p1: 0, p2: 5}
        assert not cond.resolve(products)

    def test_create_cond_from_OR_cond(self):
        cond: Condition = DiscountManagement.create_cond(self.Or_cond1)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_OR_cond2(self):
        cond: Condition = DiscountManagement.create_cond(self.Or_cond1)
        products = {p1: 0, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_Composed_AND_cond(self):
        cond_data = ['and', self.Or_cond1, self.And_cond1,
                     self.simple_cond3]  # condition should not match, because of the And_cond1
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 0, p2: 5}
        assert not cond.resolve(products)

    def test_create_cond_from_Composed_AND_cond2(self):
        cond_data = ['and', self.Or_cond1, self.And_cond1]
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_Composed_OR_cond(self):
        cond_data = ['or', self.Or_cond1, self.And_cond1]  # condition should not match, because of the And_cond1
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 0, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_Composed_OR_cond2(self):
        cond_data = ['or', self.Or_cond1, self.And_cond1]
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_Composed_OR_cond3(self):
        cond_data = ['or', self.Or_cond1, self.And_cond1, self.simple_cond3]
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    def test_create_cond_from_Composed_OR_cond4(self):
        cond_data = ['or', self.Or_cond1, self.simple_cond3, self.And_cond1]
        cond: Condition = DiscountManagement.create_cond(cond_data)
        products = {p1: 3, p2: 5}
        assert cond.resolve(products)

    ''' Add discount Tests -------------------------------------------------------------------------------- '''

    def test_add_discount_to_Empty_discount(self):
        discount = AdditiveDiscount([])
        DiscountManagement.add_discount(discount, False, None, self.product1_discount_dict1)
        p1_quantity = 3
        products = {p1: p1_quantity, p2: 5}

        assert discount.apply(products) == p1.price * p1_quantity * self.product1_discount_dict1['percentage'] / 100


    def test_add__to_Existing_discount(self):
        discount = AdditiveDiscount([])
        discount.add_discount(self.product1_discount1)
        DiscountManagement.add_discount(discount, False, None, self.product1_discount_dict2)
        products = {p1: 3, p2: 5}

        assert discount.apply(products) == (self.product1_discount1.apply(products) + self.product1_discount2.apply(products))




