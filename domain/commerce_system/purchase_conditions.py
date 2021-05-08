import datetime
import threading

from domain.commerce_system.product import Product
from typing import Dict, List

from domain.commerce_system.user import User


class Condition:

    def resolve(self) -> bool:
        raise NotImplementedError()


class ProductCondition(Condition):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class CategoryCondition(Condition):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class ShoppingBagCondition(Condition):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class UserCondition(Condition):

    def resolve(self, user: User, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class MaxQuantityForProductCondition(ProductCondition):
    def __init__(self, max_quantity: int, product: Product):
        self.max_quantity = max_quantity
        self.product = product

    def resolve(self, products: Dict[Product, int]) -> bool:
        return False if\
            self.product in products and self.max_quantity < products[self.product] \
            else True

# class UserAgeMinForCategoryCondition(UserCondition):
#     def __init__(self, min_age: int, category: str):
#         self.min_age = min_age
#         self.category = category
#
#     def resolve(self, user: User, products: Dict[Product, int]) -> bool:


class MaxTimeForCategoryCondition(CategoryCondition):
    def __init__(self, max_time: datetime, category: str):
        self.max_time = max_time
        self.category = category

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_time = datetime.now()
        for product in products:
            if product.categories.__contains__(self.category):
                if cur_time > self.max_time:
                    return False
        return True




class ANDCondition(Condition):
    def __init__(self, conditions: List[Condition]):
        self.conditions = conditions

    # returns AND between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if not cond.resolve(products):
                return False
        return True


class ORCondition(Condition):
    def __init__(self, conditions: List[Condition]):
        self.conditions = conditions

    # returns OR between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if cond.resolve(products):
                return True
        return False


class ConditioningCondition(Condition):
    def __init__(self, conditions: List[Condition]):  # expecting 2 conditions
        self.conditions = conditions

    # returns conditioning between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        if self.conditions[0].resolve(products):
            if not self.conditions[1].resolve(products):
                return False
        return True
