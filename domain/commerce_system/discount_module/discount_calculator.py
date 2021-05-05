from domain.commerce_system.product import Product
from typing import Dict, List


def calculate_total_sum(products: Dict[Product, int]) -> float:
    sum = 0
    for product in products:
        sum += product.price * products[product]
    return sum


def calculate_category_sum(products: Dict[Product, int], category: str) -> float:
    sum = 0
    for product in products:
        if product.categories.__contains__(category):
            sum += product.price * products[product]
    return sum


def calculate_product_sum(products: Dict[Product, int], product_id: int) -> float:
    for product in products:
        if product.product_id == product_id:
            return product.price * products[product]
    return 0


class Condition:

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class SimpleCondition(Condition):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class QuantitySimpleCondition(SimpleCondition):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class ProductQuantityCondition(QuantitySimpleCondition):

    def __init__(self, min_product_quantity: int, conditioned_product_id: int):
        self.min_product_quantity = min_product_quantity
        self.conditioned_product_id = conditioned_product_id

    def resolve(self, products: Dict[Product, int]) -> bool:
        for product in products:
            if product.product_id == self.conditioned_product_id:
                return products[product] >= self.min_product_quantity
        return False


class CategoryQuantityCondition(QuantitySimpleCondition):

    def __init__(self, min_category_quantity: int, conditioned_category: str):
        self.min_category_quantity = min_category_quantity
        self.conditioned_category = conditioned_category

    def resolve(self, products: Dict[Product, int]) -> bool:
        quantity = 0
        for product in products:
            if product.categories.__contains__(self.conditioned_category):
                quantity += products[product]
        return quantity >= self.min_category_quantity


class SumSimpleCondition(SimpleCondition):
    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class TotalSumCondition(SumSimpleCondition):

    def __init__(self, min_sum: int):
        self.min_sum = min_sum

    def resolve(self, products: Dict[Product, int]) -> bool:
        return calculate_total_sum(products) >= self.min_sum


class CategorySumCondition(SumSimpleCondition):

    def __init__(self, min_sum: int, conditioned_category: str):
        self.min_sum = min_sum
        self.conditioned_category = conditioned_category

    def resolve(self, products: Dict[Product, int]) -> bool:
        return calculate_category_sum(products, self.conditioned_category) >= self.min_sum


class ComposedCondition(Condition):

    def __init__(self, simple_conditions: List[SimpleCondition]):
        self.simple_conditions = simple_conditions

    # returns AND between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.simple_conditions:
            if not cond.resolve(products):
                return False
        return True


class CompleteCondition(Condition):
    def __init__(self, conditions: List[Condition]):
        self.conditions = conditions

    # returns OR between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if cond.resolve(products):
                return True
        return False


class Discount:
    def apply(self, products: Dict[Product, int]) -> float:
        raise NotImplementedError()


class ConditionalDiscount(Discount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: int):
        self.has_cond = has_cond
        self.condition = condition
        self.percentage = percentage

    def apply(self, products: Dict[Product, int]) -> float:
        raise NotImplementedError()


class ProductDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: int, product_id: int):
        super().__init__(has_cond, condition, percentage)
        self.product_id = product_id

    def apply(self, products: Dict[Product, int]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_product_sum(products, self.product_id) * self.percentage / 100
        return 0


class CategoryDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: int, category: str):
        super().__init__(has_cond, condition, percentage)
        self.category = category

    def apply(self, products: Dict[Product, int]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_category_sum(products, self.category) * self.percentage / 100
        return 0


class StoreDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: int):
        super().__init__(has_cond, condition, percentage)

    def apply(self, products: Dict[Product, int]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_total_sum(products) * self.percentage / 100
        return 0


class XorDiscount(Discount):

    def __init__(self, discounts: List[Discount]):
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
        for discount in self.discounts:
            net = discount.apply(products)
            if net > 0:
                return net
        return 0


class MaxDiscount(Discount):

    def __init__(self, discounts: List[Discount]):
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
        return max(map(lambda d: d.apply(products), self.discounts))


class AdditiveDiscount(Discount):

    def __init__(self, discounts: List[Discount]):
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
        return sum(map(lambda d: d.apply(products), self.discounts))
