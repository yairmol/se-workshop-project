from shop import Shop
from product import Product
from typing import List


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.products = {}
        self.shopping_bag_price = 0

    def add_product(self, product: Product) -> bool:
        if product in self.products:
            self.products[product] += 1
        else:
            self.products[product] = 1
        self.shopping_bag_price += product.price
        return True

    def remove_product(self, product: Product) -> bool:
        if product not in self.products:
            return False
        if self.products[product] == 1:
            self.products.pop(product)
        else:
            self.products[product] -= 1
        self.shopping_bag_price -= product.price
        return True

    def remove_all_products(self) -> bool:
        self.products.clear()
        self.shopping_bag_price = 0
        return True


class ShoppingCart:
    def __init__(self):
        self.shopping_bags = {}

    def add_shopping_bag(self, bag: ShoppingBag) -> bool:
        if bag.shop in self.shopping_bags:
            return False
        self.shopping_bags[bag.shop] = bag
        return True

    def remove_shopping_bag(self, bag: ShoppingBag) -> bool:
        if bag.shop not in self.shopping_bags:
            return False
        if not bag == self.shopping_bags[bag.shop]:
            return False
        self.shopping_bags.remove(bag.shop)
        return True

    def remove_all_shopping_bags(self) -> bool:
        self.shopping_bags.clear()
        return True
