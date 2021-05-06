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


""" ------------------------------------------------------------------------------------------- """


class Discount:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):
        self.counter_lock.acquire()
        self.discount_id = self.__id_counter
        Discount.__id_counter = Discount.__id_counter + 1
        self.counter_lock.release()

    def apply(self, products: Dict[Product, int]) -> float:
        raise NotImplementedError()


class ConditionalDiscount(Discount):
    def __init__(self, has_cond: bool, condition: Condition, percentage: int):
        super().__init__()
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
        super().__init__()
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
        for discount in self.discounts:
            net = discount.apply(products)
            if net > 0:
                return net
        return 0


class MaxDiscount(Discount):

    def __init__(self, discounts: List[Discount]):
        super().__init__()
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
        return max(map(lambda d: d.apply(products), self.discounts))


class AdditiveDiscount(Discount):

    def __init__(self, discounts: List[Discount]):
        super().__init__()
        self.discounts = discounts

    def apply(self, products: Dict[Product, int]) -> float:
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

    def delete_discounts(self, discount_ids):
        discounts_to_remove: [Discount] = []
        for discount in self.discounts:
            if discount.discount_id in discount_ids:
                discounts_to_remove.append(discount)
        for discount in discounts_to_remove:
            self.discounts.remove(discount)