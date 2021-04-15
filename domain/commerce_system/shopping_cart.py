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
    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.shopping_bags = {}
        self.shopping_cart_price = 0

    def add_product(self, product: Product, shop: Shop) -> bool:
        if shop not in self.shopping_bags:
            bag = ShoppingBag(shop)
            bag.add_product(product)
            return self.add_shopping_bag(bag)
        bag = self.shopping_bags[shop]
        if not bag.add_product(product):
            return False
        if not self.update_shopping_bag(bag):
            return False
        self.shopping_cart_price += product.price
        return True

    def update_shopping_bag(self, new_bag: ShoppingBag) -> bool:
        if new_bag.shop not in self.shopping_bags:
            return False
        if not self.remove_shopping_bag(new_bag.shop):
            return False
        return self.add_shopping_bag(new_bag)

    def add_shopping_bag(self, bag: ShoppingBag) -> bool:
        if bag.shop in self.shopping_bags:
            return False
        self.shopping_bags[bag.shop] = bag
        self.shopping_cart_price += bag.shopping_bag_price
        return True

    def remove_shopping_bag(self, shop: Shop) -> bool:
        if shop not in self.shopping_bags:
            return False
        self.shopping_cart_price -= self.shopping_bags[shop].shopping_bag_price
        self.shopping_bags.remove(shop)
        return True

    def remove_all_shopping_bags(self) -> bool:
        self.shopping_bags.clear()
        return True
