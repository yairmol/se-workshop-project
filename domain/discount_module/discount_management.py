from typing import TypedDict, Union

from domain.discount_module.discount_calculator import *


class DiscountDict(TypedDict):
    type: str  # ''' type:( 'product' / 'category' / 'shop') '''
    identifier: Union[int, str]  # identifier:( <product_id>/ <category_name>/'shop')
    percentage: int


class SimpleCond(TypedDict):
    condition: str  # condition:( 'quantity / 'sum' )
    type: str  # ''' type:( 'product' / 'category' / 'shop') '''
    identifier: Union[int, str]  # identifier:( <product_id>/ <category_name>/'shop')
    num: int  # num: (<quantity> / <sum>)


class DiscountManagement:

    @staticmethod
    def add_discount(shop_discount: AdditiveDiscount, has_cond: bool, condition: [str or SimpleCond or []],
                     new_discount_dict: DiscountDict):
        if has_cond:
            cond: Condition = DiscountManagement.create_cond(condition)
        else:
            cond = None
        discount_to_add = DiscountManagement.create_discount_from_dict(has_cond, cond, new_discount_dict)
        shop_discount.add_discount(discount_to_add)

    @staticmethod
    def create_discount_from_dict(has_cond: bool, cond: Condition, new_discount: DiscountDict) -> Discount:
        if new_discount['type'] == 'product':
            return ProductDiscount(has_cond, cond, new_discount['percentage'], new_discount['identifier'])
        if new_discount['type'] == 'category':
            return CategoryDiscount(has_cond, cond, new_discount['percentage'], new_discount['identifier'])
        if new_discount['type'] == 'product':
            return StoreDiscount(has_cond, cond, new_discount['percentage'])

    @staticmethod
    def create_cond(condition: List[Union[str, SimpleCond, List]]) -> Condition:
        if isinstance(condition[0], dict):
            return DiscountManagement.create_simple_cond(condition[0])

        if isinstance(condition[0], str):
            cond_lst = []
            for semi_cond in condition[1:len(condition)]:
                if isinstance(semi_cond, dict):
                    cond_lst.append(DiscountManagement.create_simple_cond(semi_cond))
                else:
                    cond_lst.append(DiscountManagement.create_cond(semi_cond))
            if condition[0] == 'and':
                return ANDCondition(cond_lst)
            if condition[0] == 'or':
                return ORCondition(cond_lst)

            raise Exception("Condition defined bad")



    @staticmethod
    def create_simple_cond(simple_cond: SimpleCond) -> SimpleCondition:
        if simple_cond['condition'] == 'sum':
            if simple_cond['type'] == 'category':
                return CategorySumCondition(simple_cond['num'], simple_cond['identifier'])
            if simple_cond['type'] == 'shop':
                return TotalSumCondition(simple_cond['num'])
            raise Exception("simple condition's 'type' field defined bad")

        if simple_cond['condition'] == 'quantity':
            if simple_cond['type'] == 'product':
                return ProductQuantityCondition(simple_cond['num'], simple_cond['identifier'])
            if simple_cond['type'] == 'category':
                return CategoryQuantityCondition(simple_cond['num'], simple_cond['identifier'])
            raise Exception("simple condition's 'type' field defined bad")

        raise Exception("simple condition's 'condition' field defined bad")