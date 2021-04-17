from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.shop import Shop

from typing import List, Dict


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.products: Dict[Product, int] = {}

    def add_product(self, product: Product, amount_to_buy: int):
        if product in self.products:
            self.products[product] += amount_to_buy
        else:
            self.products[product] = amount_to_buy

    def remove_product(self, product: Product, amount_to_buy: int):
        if product not in self.products:
            raise Exception("product not in the shopping bag")
        if self.products[product] < amount_to_buy:
            self.products.pop(product)
        else:
            self.products[product] -= amount_to_buy

    def remove_all_products(self):
        self.products.clear()

    def calculate_price(self) -> int:
        sum = 0
        for product, amount in self.products:
            sum += amount * product.price
        return sum

    def get_products_dtos(self):
        PRODUCT = 0
        AMOUNT = 1
        return list(map(lambda kv: ProductDTO(kv[PRODUCT], kv[AMOUNT]), self.products.items()))


class ShoppingCart:
    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.shopping_bags: Dict[Shop, ShoppingBag] = {}

    def __getitem__(self, item):
        return self.shopping_bags[item]

    def __iter__(self):
        return self.shopping_bags.items()

    def add_product(self, product: Product, shop: Shop, amount_to_buy: int):
        if shop not in self.shopping_bags:
            bag = ShoppingBag(shop)
            bag.add_product(product, amount_to_buy)
            self.add_shopping_bag(bag)
        else:
            self.add_to_shopping_bag(shop, product, amount_to_buy)

    def add_to_shopping_bag(self, shop: Shop, product: Product, amount_to_buy: int):
        self.shopping_bags[shop][product] = amount_to_buy

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
