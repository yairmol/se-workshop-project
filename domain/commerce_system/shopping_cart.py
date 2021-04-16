from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop

from typing import List


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.products = {}

    def add_product(self, product: Product):
        if product in self.products:
            self.products[product] += 1
        else:
            self.products[product] = 1

    def remove_product(self, product: Product, quantity):
        if product not in self.products:
            raise Exception("product not in the shopping bag")
        if self.products[product] < quantity:
            self.products.pop(product)
        else:
            self.products[product] -= quantity

    def remove_all_products(self):
        self.products.clear()

    def calculate_price(self) -> int:
        sum = 0
        for product, quantity in self.products:
            sum += quantity * product.price
        return sum


class ShoppingCart:
    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.shopping_bags = {}

    def add_product(self, product: Product, shop: Shop, quantity: int):
        if shop not in self.shopping_bags:
            bag = ShoppingBag(shop)
            bag.add_product(product, quantity)
            self.add_shopping_bag(bag)
        else:
            self.add_to_shopping_bag(shop, product, quantity)

    def add_to_shopping_bag(self, shop: Shop, product: Product, quantity: int):
        self.shopping_bags[shop][product] = quantity

    def add_shopping_bag(self, bag: ShoppingBag):
        if bag.shop in self.shopping_bags:
            raise Exception("bag already exists")
        self.shopping_bags[bag.shop] = bag

    def remove_shopping_bag(self, shop: Shop):
        if shop not in self.shopping_bags:
            raise Exception("no shopping bag to remove")
        self.shopping_bags.remove(shop)

    def remove_all_shopping_bags(self):
        self.shopping_bags.clear()

    def calculate_price(self):
        sum = 0
        for shop, bag in self.shopping_bags:
            sum += bag.calculate_price()
