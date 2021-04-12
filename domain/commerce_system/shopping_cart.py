from shop import Shop
from product import Product
from typing import List


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop

    def add_product(self, product: Product) -> bool:
        raise NotImplementedError()

    def remove_product(self, product: Product) -> bool:
        raise NotImplementedError()

    def remove_all_products(self) -> bool:
        raise NotImplementedError()


class ShoppingCart:
    def __init__(self):
        self.shopping_bags: List[ShoppingBag] = []

    def add_shopping_bag(self, bag: ShoppingBag) -> bool:
        raise NotImplementedError()

    def remove_shopping_bag(self, bag: ShoppingBag) -> bool:
        raise NotImplementedError()

    def remove_all_shopping_bags(self) -> bool:
        raise NotImplementedError()


