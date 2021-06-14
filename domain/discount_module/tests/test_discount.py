import unittest

from domain.commerce_system.product import BuyNow
from domain.discount_module.discount_calculator import *

product_dict1 = {"product_name": "Armani shirt", "price": 300, "description": "black shirt", "quantity": 5,
                 "categories": ['gvarim', 'dokrim']}
product_dict2 = {"product_name": "Armani Belt", "price": 100, "description": "black belt", "quantity": 10,
                 "categories": ['gvarim', 'dokrim']}
p1 = Product(**product_dict1)
p2 = Product(**product_dict2)


class DiscountTests(unittest.TestCase):

    # Product Discount Tests --------------------------------------------------------------
    def test_Product_Discount_No_Cond_Single_quantity(self):
        product_discount = ProductDiscount(False, None, 10, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 10, purchase_type)}
        assert product_discount.apply(products) == 30

    def test_Product_Discount_No_Cond_Multiplie_quantity(self):
        product_discount = ProductDiscount(False, None, 10, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 10, purchase_type),
                                                 p2: ProductInBag(p2, 10, purchase_type)}
        assert product_discount.apply(products) == 300

    def test_Product_Discount_With_Cond_Single_quantity(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)

        product_discount = ProductDiscount(True, complete_condition, 10, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 10, purchase_type)}
        assert product_discount.apply(products) == 30

    def test_Product_Discount_With_Cond_Multiplie_quantity(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)

        product_discount = ProductDiscount(True, complete_condition, 10, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 10, purchase_type)}
        assert product_discount.apply(products) == 300

    def test_Product_Discount_Failed_Cond(self):
        simple_cond = TotalSumCondition(1000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        product_discount = ProductDiscount(True, complete_condition, 10, p1.product_id)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type)}
        assert product_discount.apply(products) == 0

    # Category Discount Tests --------------------------------------------------------------------
    def test_Category_Discount_No_Cond_Single_quantity(self):
        category_dis = CategoryDiscount(False, None, 10, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type)}
        assert category_dis.apply(products) == 30

    def test_Category_Discount_No_Cond_Multiplie_quantity(self):
        category_dis = CategoryDiscount(False, None, 10, 'gvarim')
        p1_quantity = 10
        p2_quantity = 10

        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected = (p1.price * p1_quantity * (category_dis.percentage / 100)) + (
                p2.price * p2_quantity * (category_dis.percentage / 100))
        assert category_dis.apply(products) == expected

    def test_Category_Discount_With_Cond_Single_quantity(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        category_dis = CategoryDiscount(True, complete_condition, 10, 'gvarim')
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type)}

        assert category_dis.apply(products) == 30

    def test_Category_Discount_With_Cond_Multiplie_quantity(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        category_dis = CategoryDiscount(True, complete_condition, 10, 'gvarim')
        p1_quantity = 0
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected = (p1.price * p1_quantity * (category_dis.percentage / 100)) + (
                p2.price * p2_quantity * (category_dis.percentage / 100))
        assert category_dis.apply(products) == expected

    def test_Category_Discount_Failed_Cond(self):
        simple_cond = TotalSumCondition(1000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        category_discount = CategoryDiscount(True, complete_condition, 10, "gvarim")
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 3, purchase_type)}

        assert category_discount.apply(products) == 0

    # Store discount tests -----------------------------------------------------------------
    def test_Store_Discount_No_Cond_Single_Product(self):
        store_dis = StoreDiscount(False, None, 10)
        p1_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type)}

        expected = (p1.price * p1_quantity * (store_dis.percentage / 100))
        assert store_dis.apply(products) == expected

    def test_Store_Discount_No_Cond_Multiplie_Products(self):
        store_dis = StoreDiscount(False, None, 50)
        p1_quantity = 10
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected = (p1.price * p1_quantity * (store_dis.percentage / 100)) + (
                p2.price * p2_quantity * (store_dis.percentage / 100))
        assert store_dis.apply(products) == expected

    def test_Store_Discount_With_Cond_Single_Product(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 50)
        p1_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type)}

        expected = (p1.price * p1_quantity * (store_dis.percentage / 100))
        assert store_dis.apply(products) == expected

    def test_Store_Discount_With_Cond_Multiplie_Products(self):
        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 99)
        p1_quantity = 0
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}


        expected = (p1.price * p1_quantity * (store_dis.percentage / 100)) + (
                p2.price * p2_quantity * (store_dis.percentage / 100))
        assert store_dis.apply(products) == expected

    def test_Store_Discount_Failed_Cond(self):
        simple_cond = TotalSumCondition(1000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 99)
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 3, purchase_type)}

        assert store_dis.apply(products) == 0

    # XOR discount tests ---------------------------------------------------------
    def test_XorDiscount_Single_Discount_With_No_cond(self):
        store_dis = StoreDiscount(False, None, 50)
        discount_lst = [store_dis]
        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected_discount = xor_dis.discounts[0]
        expected_dis_sum = expected_discount.apply(products)
        assert xor_dis.apply(products) == expected_dis_sum

    def test_XorDiscount_Single_Discount_With_cond(self):
        simple_cond = TotalSumCondition(1000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 50)

        discount_lst = [store_dis]
        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected_discount = xor_dis.discounts[0]
        expected_dis_sum = expected_discount.apply(products)
        assert xor_dis.apply(products) == expected_dis_sum

    def test_XorDiscount_Single_Discount_With_FAILED_cond(self):
        simple_cond = TotalSumCondition(10000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 50)

        discount_lst = [store_dis]
        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected_discount = xor_dis.discounts[0]
        expected_dis_sum = expected_discount.apply(products)

        assert xor_dis.apply(products) == expected_dis_sum

    def test_XorDiscount_Multiplie_Discount_With_No_cond(self):
        store_dis = StoreDiscount(False, None, 50)
        category_dis = CategoryDiscount(False, None, 10, 'gvarim')
        discount_lst = [store_dis, category_dis]
        expected_discount = discount_lst[0]

        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected_dis_sum = expected_discount.apply(products)
        assert xor_dis.apply(products) == expected_dis_sum

    def test_XorDiscount_Multiplie_Discount_With_cond(self):
        simple_cond = TotalSumCondition(1000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 50)  # first discount

        simple_cond = TotalSumCondition(100)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        category_dis = CategoryDiscount(True, complete_condition, 10, 'gvarim')  # second discount

        discount_lst = [category_dis, store_dis]
        expected_discount = discount_lst[0]

        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected_dis_sum = expected_discount.apply(products)
        assert xor_dis.apply(products) == expected_dis_sum

    def test_XorDiscount_Multiplie_Discount_With_FAILED_cond(self):
        simple_cond = TotalSumCondition(100000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        store_dis = StoreDiscount(True, complete_condition, 50)  # first discount

        simple_cond = TotalSumCondition(100000)
        cond_lst = [simple_cond]
        complete_condition = ORCondition(cond_lst)
        category_dis = CategoryDiscount(True, complete_condition, 10, 'gvarim')  # second discount

        discount_lst = [category_dis, store_dis]
        xor_dis = XorDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        assert xor_dis.apply(products) == 0

    def test_AdditiveDiscount_Single_Discount(self):
        store_dis = StoreDiscount(False, None, 50)
        discount_lst = [store_dis]
        additive_discount = AdditiveDiscount(discount_lst)

        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected_dis_sum = store_dis.apply(products)

        assert additive_discount.apply(products) == expected_dis_sum

    def test_AdditiveDiscount_Multiplie_Discount(self):
        store_dis = StoreDiscount(False, None, 10)
        category_dis = CategoryDiscount(False, None, 10, 'gvarim')
        discount_lst = [store_dis, category_dis]
        additive_discount = AdditiveDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected_dis_sum = store_dis.apply(products) + category_dis.apply(products)
        assert additive_discount.apply(products) == expected_dis_sum

    def test_MaxDiscount_Single_Discount(self):
        store_dis = StoreDiscount(False, None, 50)
        discount_lst = [store_dis]
        max_discount = MaxDiscount(discount_lst)

        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}
        expected_dis_sum = store_dis.apply(products)

        assert max_discount.apply(products) == expected_dis_sum

    def test_MaxDiscount_Multiplie_Discount(self):
        store_dis = StoreDiscount(False, None, 10)
        category_dis = CategoryDiscount(False, None, 10, 'gvarim')
        discount_lst = [store_dis, category_dis]
        max_discount = MaxDiscount(discount_lst)
        p1_quantity = 5
        p2_quantity = 10
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, p1_quantity, purchase_type),
                                                 p2: ProductInBag(p2, p2_quantity, purchase_type)}

        expected_dis_sum = max(store_dis.apply(products), category_dis.apply(products))
        assert max_discount.apply(products) == expected_dis_sum

    '''Discount Aggregation tests '''

    def test_Max_Aggregation(self):
        main_discount = AdditiveDiscount([])
        discount1 = StoreDiscount(False, None, 10)
        discount2 = CategoryDiscount(False, None, 15, 'gvarim')
        main_discount.add_discount(discount1)
        main_discount.add_discount(discount2)
        main_discount.aggregate_discounts([discount1.discount_id, discount2.discount_id], "max")
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}

        assert main_discount.apply(products) == max(discount1.apply(products), discount2.apply(products))

    def test_Max_Aggregation2(self):
        main_discount = AdditiveDiscount([])
        discount1 = StoreDiscount(False, None, 10)
        discount2 = CategoryDiscount(False, None, 15, 'gvarim')
        discount3 = ProductDiscount(False, None, 5, p1.product_id)

        main_discount.add_discount(discount1)
        main_discount.add_discount(discount2)
        main_discount.add_discount(discount3)
        main_discount.aggregate_discounts([discount1.discount_id, discount2.discount_id], "max")
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}

        assert main_discount.apply(products) == (max(discount1.apply(products), discount2.apply(products)) + discount3.apply(products))

    def test_Xor_Aggregation(self):
        main_discount = AdditiveDiscount([])
        discount1 = StoreDiscount(False, None, 10)
        discount2 = CategoryDiscount(False, None, 15, 'gvarim')
        main_discount.add_discount(discount1)
        main_discount.add_discount(discount2)
        main_discount.aggregate_discounts([discount1.discount_id, discount2.discount_id], "xor")
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}

        assert main_discount.apply(products) in (discount1.apply(products), discount2.apply(products))

    def test_Add_Aggregation(self):
        main_discount = AdditiveDiscount([])
        discount1 = StoreDiscount(False, None, 10)
        discount2 = CategoryDiscount(False, None, 15, 'gvarim')
        main_discount.add_discount(discount1)
        main_discount.add_discount(discount2)
        main_discount.aggregate_discounts([discount1.discount_id, discount2.discount_id], "add")
        purchase_type = p1.get_purchase_type_of_type(BuyNow)
        products: Dict[Product, ProductInBag] = {p1: ProductInBag(p1, 1, purchase_type),
                                                 p2: ProductInBag(p2, 1, purchase_type)}

        assert main_discount.apply(products) == discount1.apply(products) + discount2.apply(products)
