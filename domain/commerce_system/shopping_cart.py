from datetime import datetime

from domain.commerce_system.action import Action, ActionPool
from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.purchase_conditions import ANDCondition
from domain.commerce_system.shop import Shop

from typing import Dict, List

from domain.commerce_system.transaction import Transaction
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.payment_module.payment_system import IPaymentsFacade

CART_ID = "cart_id"
SHOPPING_BAGS = "shopping_bags"
PRODUCTS = "products"
SHOP_NAME = "shop_name"
TOTAL = "total"


class ShoppingBag:
    def __init__(self, shop: Shop):
        self.shop = shop
        self.products: Dict[Product, int] = {}
        self.payment_facade = IPaymentsFacade.get_payment_facade()
        self.delivery_facade = IDeliveryFacade.get_delivery_facade()

    def __setitem__(self, key: Product, value: int):
        self.products[key] = value

    def __iter__(self):
        return self.products.items().__iter__()

    def to_dict(self):
        return {
            SHOP_NAME: self.shop.name,
            PRODUCTS: [ProductDTO(prod, amount).to_dict() for prod, amount in self.products.items()],
            TOTAL: self.calculate_price()
        }

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
        for product, amount in self.products.items():
            total += amount * product.price
        total = max(0, total - self.shop.discount.apply(self.products))
        return total

    def get_products_dtos(self):
        PRODUCT = 0
        AMOUNT = 1
        return list(map(lambda kv: ProductDTO(kv[PRODUCT], kv[AMOUNT]), self.products.items()))

    def set_products(self, products: Dict[Product, int]) -> bool:
        self.products = products
        return True

    def clear_bag(self) -> bool:
        self.products.clear()
        return True

    def resolve_shop_conditions(self) -> bool:
        conditions = ANDCondition({"conditions": self.shop.conditions})
        return conditions.resolve(self.products)

    def purchase_bag(self, username, payment_details) -> Transaction:
        assert self.resolve_shop_conditions(), f"condition exception: {self}"
        total_price = self.calculate_price()
        products_dtos = self.get_products_dtos()
        transaction = Transaction(
            username, self.shop, products_dtos, payment_details,
            datetime.now(), total_price
        )

        shop_action = Action(self.shop.add_transaction, self, transaction)
        shop_action.set_reverse(Action(self.shop.cancel_transaction, self, transaction))
        payment_action = Action(self.payment_facade.pay, total_price, payment_details)
        payment_action.set_reverse(Action(self.payment_facade.cancel_payment), True)
        delivery_action = Action(self.delivery_facade.deliver_to, [p.to_dict() for p in products_dtos], "")
        delivery_action.set_reverse(Action(self.delivery_facade.cancel_delivery), use_return_value=True)
        clean_action = Action(self.clear_bag).set_reverse(Action(self.set_products, self.products.copy()))

        purchase_actions = ActionPool([shop_action, payment_action, delivery_action, clean_action])
        transaction.set_transaction_action_pool(purchase_actions)
        assert purchase_actions.execute_actions(), f"couldn't purchase bag: {self}"
        return transaction

    @staticmethod
    def cancel_transaction(transaction):
        transaction.cancel_transaction()


class ShoppingCart:
    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.shopping_bags: Dict[Shop, ShoppingBag] = {}

    def __getitem__(self, item):
        return self.shopping_bags[item]

    def __iter__(self):
        return self.shopping_bags.items().__iter__()

    def to_dict(self) -> dict:
        return {
            SHOPPING_BAGS: {shop.shop_id: sb.to_dict() for shop, sb in self.shopping_bags.items()},
            CART_ID: self.cart_id,
            TOTAL: self.calculate_price(),
        }

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

    def remove_shopping_bags(self, shops):
        for shop in shops:
            self.remove_shopping_bag(shop)
        return True

    def calculate_price(self):
        total = 0
        for shop, bag in self.shopping_bags.items():
            total += bag.calculate_price()
        return total

    def _purchase_shopping_bag(self, username: str, bag: ShoppingBag, payment_details, purchased_shops: list):
        transaction = bag.purchase_bag(username, payment_details)
        purchased_shops.append(bag.shop)
        return transaction

    def purchase_cart(self, username: str, payment_details: dict, do_what_you_can: bool = False) -> List[Transaction]:
        purchased_shops = []
        actions = ActionPool([
                                 Action(self._purchase_shopping_bag, username, bag, payment_details, purchased_shops)
                             .set_reverse(Action(ShoppingBag.cancel_transaction), use_return_value=True)
                                 for shop, bag in self
                             ] + [Action(self.remove_shopping_bags, purchased_shops)])
        assert actions.execute_actions(do_what_you_can)
        return actions.get_return_values()[:-1]
