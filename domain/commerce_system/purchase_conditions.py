from datetime import datetime, time
import threading

from domain.commerce_system.product import Product
from typing import Dict, List


# from domain.commerce_system.user import User


class Condition:
    __id_counter = 1
    counter_lock = threading.Lock()

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


# class UserCondition(Condition):
#
#     def resolve(self, user: User, products: Dict[Product, int]) -> bool:
#         raise NotImplementedError()


class MaxQuantityForProductCondition(ProductCondition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.max_quantity = condition_dict["max_quantity"]
        self.product = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        return False if \
            self.product in products and self.max_quantity < products[self.product] \
            else True


# class UserAgeMinForCategoryCondition(UserCondition):
#     def __init__(self, min_age: int, category: str):
#         self.min_age = min_age
#         self.category = category
#
#     def resolve(self, user: User, products: Dict[Product, int]) -> bool:


class TimeWindowForCategoryCondition(CategoryCondition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.min_time = condition_dict["min_time"]
        self.max_time = condition_dict["max_time"]
        self.category = condition_dict["category"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_time = datetime.now().time()
        for product in products:
            if product.categories.__contains__(self.category):
                if cur_time > self.max_time or cur_time < self.min_time:
                    return False
        return True


class TimeWindowForProductCondition(CategoryCondition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.min_time = condition_dict["min_time"]
        self.max_time = condition_dict["max_time"]
        self.product = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_time = datetime.now().time()
        if self.product in products:
            if cur_time > self.max_time or cur_time < self.min_time:
                return False
        return True


class DateWindowForCategoryCondition(CategoryCondition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.min_date = condition_dict["min_date"]
        self.max_date = condition_dict["max_date"]
        self.category = condition_dict["category"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_date = datetime.now()
        for product in products:
            if product.categories.__contains__(self.category):
                if cur_date > self.max_date or cur_date < self.min_date:
                    return False
        return True


class DateWindowForProductCondition(CategoryCondition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.min_date = condition_dict["min_date"]
        self.max_date = condition_dict["max_date"]
        self.product = condition_dict["product"]

    def resolve(self, products: Dict[Product, int]) -> bool:
        cur_date = datetime.now()
        if self.product in products:
            if cur_date > self.max_date or cur_date < self.min_date:
                return False
        return True


class ANDCondition(Condition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.conditions = condition_dict["conditions"]

    # returns AND between all conditions
    def resolve(self, products: Dict[Product, int]) -> bool:
        for cond in self.conditions:
            if not cond.resolve(products):
                return False
        return True


class ORCondition(Condition):
    def __init__(self, condition_dict: dict):
        self.counter_lock.acquire()
        self.id = self.__id_counter
        Condition.__id_counter = Condition.__id_counter + 1
        self.counter_lock.release()
        self.conditions = condition_dict["conditions"]

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
