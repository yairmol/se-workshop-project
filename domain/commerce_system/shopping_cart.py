from shop import Shop
from product import Product
from typing import List


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.shopping_bag = {}
        self.shopping_bag_price = 0

    def add_product(self, product: Product) -> bool:
        if product in self.shopping_bag:
            self.shopping_bag[product] += 1
        else:
            self.shopping_bag[product] = 1
        self.shopping_bag_price += product.price
        return True

    def remove_product(self, product: Product) -> bool:
        if product not in self.shopping_bag:
            return False
        if self.shopping_bag[product] == 1:
            self.shopping_bag.pop(product)
        else:
            self.shopping_bag[product] -= 1
        self.shopping_bag_price -= product.price
        return True

    def remove_all_products(self) -> bool:
        self.shopping_bag.clear()
        self.shopping_bag_price = 0
        return True


class ShoppingCart:
    def __init__(self):
        self.shopping_bags: List[ShoppingBag] = []

    def add_shopping_bag(self, bag: ShoppingBag) -> bool:
        self.shopping_bags += [bag]
        return True

    def remove_shopping_bag(self, bag: ShoppingBag) -> bool:
        if bag not in self.shopping_bags:
            return False
        self.shopping_bags.remove(bag)
        return True

    def remove_all_shopping_bags(self) -> bool:
        self.shopping_bags.clear()
        return True
