from abc import ABC
from datetime import datetime
import threading

from domain.commerce_system.product import Product
from typing import Dict
from data_model import ConditionsModel as CondM

# from domain.commerce_system.user import User


class Condition:
    _id_counter = 1
    counter_lock = threading.Lock()
    type = None

    def __init__(self):
        with Condition.counter_lock:
            self.id = Condition._id_counter
            Condition._id_counter += 1

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class ProductCondition(Condition, ABC):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class CategoryCondition(Condition, ABC):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


class ShoppingBagCondition(Condition, ABC):

    def resolve(self, products: Dict[Product, int]) -> bool:
        raise NotImplementedError()


# class UserCondition(Condition):
#
#     def resolve(self, user: User, products: Dict[Product, int]) -> bool:
#         raise NotImplementedError()


class MaxQuantityForProductCondition(ProductCondition):
    type = CondM.MAX_QUANTITY_FOR_PRODUCT

    def __init__(self, condition_dict: dict):
        super().__init__()
        self.max_quantity = condition_dict["max_quantity"]
        self.product_id = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        for product in products:
            if product.product_id == self.product_id:
                if self.max_quantity < products[product]:
                    return False
        return True

    def to_dict(self):
        return {}


# class UserAgeMinForCategoryCondition(UserCondition):
#     def __init__(self, min_age: int, category: str):
#         self.min_age = min_age
#         self.category = category
#
#     def resolve(self, user: User, products: Dict[Product, int]) -> bool:


class TimeWindowForCategoryCondition(CategoryCondition):
    type = CondM.TIME_WINDOW_FOR_CATEGORY

    def __init__(self, condition_dict: dict):
        super().__init__()
        self.min_time = datetime.strptime(condition_dict["min_time"], '%H:%M').time()
        self.max_time = datetime.strptime(condition_dict["max_time"], '%H:%M').time()
        self.category = condition_dict["category"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_time = datetime.now().time()
        for product in products:
            if product.categories.__contains__(self.category):
                if cur_time > self.max_time or cur_time < self.min_time:
                    return False
        return True

    def to_dict(self):
        return {}


class TimeWindowForProductCondition(CategoryCondition):
    type = CondM.TIME_WINDOW_FOR_PRODUCT

    def __init__(self, condition_dict: dict):
        super().__init__()
        self.min_time = datetime.strptime(condition_dict["min_time"], '%H:%M').time()
        self.max_time = datetime.strptime(condition_dict["max_time"], '%H:%M').time()
        self.product_id = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_time = datetime.now().time()
        for product in products:
            if product.product_id == self.product_id:
                if cur_time > self.max_time or cur_time < self.min_time:
                    return False
        return True

    def to_dict(self):
        return {}


class DateWindowForCategoryCondition(CategoryCondition):
    type = CondM.DATE_WINDOW_FOR_CATEGORY

    def __init__(self, condition_dict: dict):
        super().__init__()
        self.min_date = datetime.strptime(condition_dict["min_date"], '%d/%m/%Y')
        self.max_date = datetime.strptime(condition_dict["max_date"], '%d/%m/%Y')
        self.category = condition_dict["category"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_date = datetime.now()
        for product in products:
            if product.categories.__contains__(self.category):
                if cur_date > self.max_date or cur_date < self.min_date:
                    return False
        return True

    def to_dict(self):
        return {}


class DateWindowForProductCondition(CategoryCondition):
    type = CondM.DATE_WINDOW_FOR_PRODUCT

    def __init__(self, condition_dict: dict):
        super().__init__()
        self.min_date = datetime.strptime(condition_dict["min_date"], '%d/%m/%Y')
        self.max_date = datetime.strptime(condition_dict["max_date"], '%d/%m/%Y')
        self.product_id = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_date = datetime.now()
        for product in products:
            if product.product_id == self.product_id:
                if cur_date > self.max_date or cur_date < self.min_date:
                    return False
        return True

    def to_dict(self):
        return {}


class CompositePurchaseCondition(Condition, ABC):
    def __init__(self, condition_dict: dict):
        super().__init__()
        self.conditions = condition_dict["conditions"]

    def to_dict(self):
        return {
            "conditions": [c.to_dict() for c in self.conditions]
        }


class ANDCondition(CompositePurchaseCondition):
    type = CondM.AND_CONDITION

    # returns AND between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if not cond.resolve(products):
                return False
        return True


class ORCondition(CompositePurchaseCondition):
    type = CondM.OR_CONDITION
    # returns OR between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if cond.resolve(products):
                return True
        return False

# class ConditioningCondition(Condition):
#     def __init__(self, conditions: List[Condition]):  # expecting 2 conditions
#         self.conditions = conditions
#
#     # returns conditioning between all conditions
#     def resolve(self, products: Dict[Product, int]) -> bool:
#         if self.conditions[0].resolve(products):
#             if not self.conditions[1].resolve(products):
#                 return False
#         return True
