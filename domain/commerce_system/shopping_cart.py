from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.shop import Shop

from typing import Dict


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.products: Dict[Product, int] = {}

    def __setitem__(self, key: Product, value: int):
        self.products[key] = value

    def add_product(self, product: Product, amount_to_buy: int):
        if product in self.products:
            self.products[product] += amount_to_buy
        else:
            self.products[product] = amount_to_buy

    def remove_product(self, product: Product, amount_to_buy: int):
        assert product in self.products, "product not in the shopping bag"
        assert self.products[product] >= amount_to_buy, "not enough items in the bag"
        if self.products[product] == amount_to_buy:
            self.products.pop(product)
        else:
            self.products[product] -= amount_to_buy

    def remove_all_products(self):
        self.products.clear()

    def calculate_price(self) -> int:
        total = 0
        for product, amount in self.products:
            total += amount * product.price
        return total

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
        return self.shopping_bags.items().__iter__()

    def add_product(self, product: Product, shop: Shop, amount_to_buy: int):
        if shop not in self.shopping_bags:
            bag = ShoppingBag(shop)
            bag.add_product(product, amount_to_buy)
            self.add_shopping_bag(bag)
        else:
            self.add_to_shopping_bag(shop, product, amount_to_buy)
        return True

    def add_to_shopping_bag(self, shop: Shop, product: Product, amount_to_buy: int):
        self.shopping_bags[shop].add_product(product, amount_to_buy)

    def remove_from_shopping_bag(self, shop: Shop, product: Product, amount: int):
        self.shopping_bags[shop].remove_product(product, amount)

    def add_shopping_bag(self, bag: ShoppingBag):
        assert bag.shop not in self.shopping_bags, "bag already exists"
        self.shopping_bags[bag.shop] = bag

    def remove_shopping_bag(self, shop: Shop):
        assert shop in self.shopping_bags, "no shopping bag to remove"
        self.shopping_bags.pop(shop)

    def remove_all_shopping_bags(self):
        self.shopping_bags.clear()

    def calculate_price(self):
        total = 0
        for shop, bag in self.shopping_bags:
            total += bag.calculate_price()
