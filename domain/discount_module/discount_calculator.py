import threading
from abc import ABC

from domain.commerce_system.product import Product, ProductInBag
from typing import Dict, List, Union


def calculate_total_sum(products: Dict[Product, ProductInBag]) -> float:
    _sum = 0
    for product, bag_info in products.items():
        _sum += product.price * bag_info.amount
    return _sum


def calculate_category_sum(products: Dict[Product, ProductInBag], category: str) -> float:
    _sum = 0
    for product, bag_info in products.items():
        if category in product.get_category_names():
            _sum += product.price * bag_info.amount
    return _sum


def calculate_product_sum(products: Dict[Product, ProductInBag], product_id: int) -> float:
    for product, bag_info in products.items():
        if product.product_id == product_id:
            return product.price * bag_info.amount
    return 0


class Condition:

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class SimpleCondition(Condition):

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class QuantitySimpleCondition(SimpleCondition):

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class ProductQuantityCondition(QuantitySimpleCondition):

    def __init__(self, min_product_quantity: Union[str, int], conditioned_product_id: Union[str, int]):
        self.type = "ProductQuantityCondition"
        self.minimum = int(min_product_quantity)
        self.conditioned_product_id = int(conditioned_product_id)

    def to_dict(self):
        return {
            "condition": "quantity",
            "type": "product",
            "identifier": self.conditioned_product_id,
            "num": self.minimum
        }

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        for product, bag_info in products.items():
            if product.product_id == self.conditioned_product_id:
                return bag_info.amount >= self.minimum
        return False


class CategoryQuantityCondition(QuantitySimpleCondition):

    def __init__(self, min_category_quantity: Union[int, str], conditioned_category: str):
        self.type = "CategoryQuantityCondition"
        self.minimum = int(min_category_quantity)
        self.conditioned_category = conditioned_category

    def to_dict(self):
        return {
            "condition": "quantity",
            "type": "category",
            "identifier": self.conditioned_category,
            "num": self.minimum
        }

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        quantity = 0
        for product, bag_info in products.items():
            if self.conditioned_category in product.get_category_names():
                quantity += bag_info.amount
        return quantity >= self.minimum


class SumSimpleCondition(SimpleCondition, ABC):

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        raise NotImplementedError()


class TotalSumCondition(SumSimpleCondition):

    def __init__(self, min_sum: Union[str, int, float]):
        self.type = "TotalSumCondition"
        self.minimum = float(min_sum)

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        return calculate_total_sum(products) >= self.minimum

    def to_dict(self):
        return {
            "condition": "sum",
            "type": "shop",
            "identifier": None,
            "num": self.minimum
        }


class CategorySumCondition(SumSimpleCondition):

    def __init__(self, min_sum: int, conditioned_category: str):
        self.type = "CategorySumCondition"
        self.minimum = float(min_sum)
        self.conditioned_category = conditioned_category

    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        return calculate_category_sum(products, self.conditioned_category) >= self.minimum

    def to_dict(self):
        return {
            "condition": "sum",
            "type": "category",
            "identifier": self.conditioned_category,
            "num": self.minimum
        }


class ANDCondition(Condition):

    def __init__(self, conditions: List[Condition]):
        self.type = "ANDCondition"
        self.conditions = conditions

    # returns AND between all conditions
    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        for cond in self.conditions:
            if not cond.resolve(products):
                return False
        return True

    def to_dict(self):
        return ["and"] + [c.to_dict() for c in self.conditions]


class ORCondition(Condition):
    def __init__(self, conditions: List[Condition]):
        self.type = "ORCondition"
        self.conditions = conditions

    # returns OR between all conditions
    def resolve(self, products: Dict[Product, ProductInBag]) -> bool:
        for cond in self.conditions:
            if cond.resolve(products):
                return True
        return False

    def to_dict(self):
        return ["or"] + [c.to_dict() for c in self.conditions]


""" ------------------------------------------------------------------------------------------- """


class Discount:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):
        self.counter_lock.acquire()
        self.discount_id = self.__id_counter
        Discount.__id_counter = Discount.__id_counter + 1
        self.counter_lock.release()

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class ConditionalDiscount(Discount, ABC):
    def __init__(self, has_cond: bool, condition: Condition, percentage: Union[str, float]):
        super().__init__()
        self.has_cond = has_cond
        self.condition = condition
        self.percentage = float(percentage)

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        raise NotImplementedError()


class ProductDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: Union[str, float], product_id: Union[int, str]):
        super().__init__(has_cond, condition, percentage)
        self.type = "ProductDiscount"
        self.product_id = int(product_id)

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_product_sum(products, self.product_id) * self.percentage / 100
        return 0

    def to_dict(self):
        return {
            "id": self.discount_id,
            "composite": False,
            "condition": self.condition.to_dict() if self.condition else [],
            "type": "product",
            "identifier": self.product_id,
            "percentage": self.percentage,
        }


class CategoryDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: Union[str, float], category: str):
        super().__init__(has_cond, condition, percentage)
        self.type = "CategoryDiscount"
        self.category = category

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_category_sum(products, self.category) * self.percentage / 100
        return 0

    def to_dict(self):
        return {
            "id": self.discount_id,
            "composite": False,
            "condition": self.condition.to_dict() if self.condition else [],
            "type": "category",
            "identifier": self.category,
            "percentage": self.percentage,
        }


class StoreDiscount(ConditionalDiscount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: Union[str, float]):
        super().__init__(has_cond, condition, percentage)
        self.type = "StoreDiscount"

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        if (not self.has_cond) or self.condition.resolve(products):
            return calculate_total_sum(products) * self.percentage / 100
        return 0

    def to_dict(self):
        return {
            "id": self.discount_id,
            "composite": False,
            "condition": self.condition.to_dict() if self.condition else [],
            "type": "shop",
            "identifier": None,
            "percentage": self.percentage
        }


class CompositeDiscount(Discount):
    def __init__(self, discounts: List[Discount]):
        super().__init__()
        self.discounts = discounts

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        raise NotImplementedError()

    def to_dict(self):
        return {
            "id": self.discount_id,
            "composite": True,
            "operator": self.get_operator(),
            "discounts": [d.to_dict() for d in self.discounts]
        }

    def get_operator(self):
        raise NotImplementedError()


class XorDiscount(CompositeDiscount):
    def __init__(self, discounts: List[Discount]):
        super().__init__(discounts)
        self.type = "XorDiscount"

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        for discount in self.discounts:
            net = discount.apply(products)
            if net > 0:
                return net
        return 0

    def get_operator(self):
        return "xor"


class MaxDiscount(CompositeDiscount):
    def __init__(self, discounts: List[Discount]):
        super().__init__(discounts)
        self.type = "MaxDiscount"

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        return max(map(lambda d: d.apply(products), self.discounts))

    def get_operator(self):
        return "max"


class AdditiveDiscount(CompositeDiscount):
    def __init__(self, discounts: List[Discount]):
        super().__init__(discounts)
        self.type = "AdditiveDiscount"

    def apply(self, products: Dict[Product, ProductInBag]) -> float:
        return sum(map(lambda d: d.apply(products), self.discounts))

    def add_discount(self, discount: Discount):
        self.discounts.append(discount)

    def aggregate_discounts(self, discount_ids: [int], func: str):

        discounts_to_aggregate: [Discount] = []
        for discount in self.discounts:
            if discount.discount_id in discount_ids:
                discounts_to_aggregate.append(discount)
        for discount in discounts_to_aggregate:
            self.discounts.remove(discount)

        if func == "max":
            self.discounts.append(MaxDiscount(discounts_to_aggregate))
        if func == "xor":
            self.discounts.append(XorDiscount(discounts_to_aggregate))
        if func == "add":
            self.discounts.append(AdditiveDiscount(discounts_to_aggregate))

    def get_operator(self):
        return "additive"
