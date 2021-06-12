
import threading
from datetime import datetime

from sqlalchemy import orm

from data_access_layer.engine import add_to_session, add_shop_to_session, save, delete
from domain.commerce_system.action import Action, ActionPool
from domain.commerce_system.product import Product, BuyNow, PurchaseType, ProductInBag
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.purchase_conditions import ANDCondition
from domain.commerce_system.shop import Shop

from typing import Dict, List, TypeVar, Optional

from domain.commerce_system.transaction import Transaction
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.payment_module.payment_system import IPaymentsFacade

CART_ID = "cart_id"
SHOPPING_BAGS = "shopping_bags"
PRODUCTS = "products"
SHOP_NAME = "shop_name"
TOTAL = "total"


T_PT = TypeVar('T_PT', bound=PurchaseType)


class ShoppingBag:
    __bag_id = 1
    __idlock = threading.Lock()

    def __init__(self, shop: Shop):
        with ShoppingBag.__idlock:
            self.bag_id = ShoppingBag.__bag_id
            ShoppingBag.__bag_id += 1
        self.shop = shop
        self.products: Dict[Product, ProductInBag] = {}
        self.payment_facade = IPaymentsFacade.get_payment_facade()
        self.delivery_facade = IDeliveryFacade.get_delivery_facade()

    @orm.reconstructor
    def init_on_load(self):
        self.payment_facade = IPaymentsFacade.get_payment_facade()
        self.delivery_facade = IDeliveryFacade.get_delivery_facade()

    def __setitem__(self, key: Product, value: ProductInBag):
        self.products[key] = value

    def __iter__(self):
        return self.products.items().__iter__()

    def to_dict(self):
        return {
            SHOP_NAME: self.shop.name,
            PRODUCTS: [
                ProductDTO(prod, prod_in_bag).to_dict()
                for prod, prod_in_bag in self.products.items()
            ],
            TOTAL: self.calculate_price()
        }

    def add_product(self, product: Product, amount_to_buy: int,
                    purchase_type_id: Optional[int] = None, **purchase_type_args):
        if product in self.products:
            self.products[product].amount += amount_to_buy
            save(ProductInBag, self.products[product])
        else:
            purchase_type = product.get_purchase_type_of_type(BuyNow)
            if purchase_type_id:
                purchase_type = product.get_purchase_type(purchase_type_id)
            pib = ProductInBag(product, amount_to_buy, purchase_type, **purchase_type_args)
            save(ProductInBag, pib)
            self.products[product] = pib

    def remove_product(self, product: Product, amount_to_buy: int):
        assert product in self.products, "product not in the shopping bag"
        assert self.products[product].amount >= amount_to_buy, "not enough items in the bag"
        if self.products[product].amount == amount_to_buy:
            delete(ProductInBag, self.products[product])
            self.products.pop(product)
        else:
            save(ProductInBag, self.products[product])
            self.products[product].amount -= amount_to_buy

    def remove_all_products(self):
        self.products.clear()

    def calculate_price(self) -> int:
        total = 0
        for product, prod_in_bag in self.products.items():
            total += prod_in_bag.amount * prod_in_bag.purchase_type.get_price(**prod_in_bag.purchase_type_args)
        total = max(0, total - self.shop.discount.apply(self.products))
        return total

    def get_products_dtos(self):
        product = 0
        bag_info = 1
        return list(map(lambda kv: ProductDTO(kv[product], kv[bag_info]), self.products.items()))

    def set_products(self, products: Dict[Product, ProductInBag]) -> bool:
        self.products = products
        save(ShoppingBag, self)
        return True

    def clear_bag(self) -> bool:
        self.products.clear()
        save(ShoppingBag, self)
        return True

    def resolve_shop_conditions(self) -> bool:
        conditions = ANDCondition({"conditions": self.shop.conditions})
        return conditions.resolve({k: v.amount for k, v in self.products.items()})

    def purchase_bag(self, username, payment_details, delivery_details: dict) -> Transaction:
        assert self.resolve_shop_conditions(), f"condition exception: {self}"
        assert all(
            bag_info.purchase_type.can_purchase(**bag_info.purchase_type_args)
            for bag_info in self.products.values()
        ), "cannot purchase bag"
        total_price = self.calculate_price()
        products_dtos = self.get_products_dtos()
        transaction = Transaction(
            username, self.shop, products_dtos, payment_details,
            datetime.now(), total_price
        )

        shop_action = Action(self.shop.add_transaction, self, transaction)
        shop_action.set_reverse(Action(self.shop.cancel_transaction, self, transaction))
        shop_action.set_error_message("failed to save transaction")
        payment_action = Action(self.payment_facade.pay, total_price, payment_details)
        payment_action.set_reverse(Action(self.payment_facade.cancel_payment), True)
        payment_action.set_error_message("payment failed")
        delivery_action = Action(self.delivery_facade.deliver_to, delivery_details)
        delivery_action.set_reverse(Action(self.delivery_facade.cancel_delivery), use_return_value=True)
        delivery_action.set_error_message("delivery failed")
        clean_action = Action(self.clear_bag).set_reverse(Action(self.set_products, self.products.copy()))
        clean_action.set_error_message("failed to clear shopping bag")

        purchase_actions = ActionPool([shop_action, payment_action, delivery_action, clean_action])
        transaction.set_transaction_action_pool(purchase_actions)
        assert purchase_actions.execute_actions(), f"couldn't purchase bag: {self}"
        return transaction

    @staticmethod
    def cancel_transaction(transaction):
        transaction.cancel_transaction()

    def change_product_purchase_type(self, product: Product, purchase_type_id: int, pt_args: dict) -> bool:
        assert purchase_type_id in product.purchase_types, "purchase type doesn't exist"
        # if we can get the price then it is valid for the cart owner to set this purchase type.
        product.purchase_types[purchase_type_id].get_price(**pt_args)
        self.products[product].purchase_type = product.purchase_types[purchase_type_id]
        self.products[product].purchase_type_args = pt_args
        save(ShoppingBag, self.products[product])
        return True


class ShoppingCart:
    __cart_id = 1
    __idlock = threading.Lock()

    def __init__(self):
        with ShoppingCart.__idlock:
            self.cart_id = ShoppingCart.__cart_id
            ShoppingCart.__cart_id += 1
        self.shopping_bags: Dict[Shop, ShoppingBag] = {}
        self.of_subscribed = False

    @orm.reconstructor
    def init_on_load(self):
        self.of_subscribed = True

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

    def add_product(self, product: Product, shop: Shop, amount_to_buy: int, purchase_type_id=None, **pt_args):
        if shop not in self.shopping_bags:
            bag = ShoppingBag(shop)
            bag.add_product(product, amount_to_buy, purchase_type_id, **pt_args)
            self.add_shopping_bag(bag)
        else:
            self.add_to_shopping_bag(shop, product, amount_to_buy, purchase_type_id, **pt_args)
        return True

    def add_to_shopping_bag(self, shop: Shop, product: Product, amount_to_buy: int, purchase_type_id=None, **pt_args):
        self.shopping_bags[shop].add_product(product, amount_to_buy, purchase_type_id, **pt_args)

    def remove_from_shopping_bag(self, shop: Shop, product: Product, amount: int):
        self.shopping_bags[shop].remove_product(product, amount)

    def add_shopping_bag(self, bag: ShoppingBag):
        assert bag.shop not in self.shopping_bags, "bag already exists"
        save(bag)
        self.shopping_bags[bag.shop] = bag

    def remove_shopping_bag(self, shop: Shop):
        assert shop in self.shopping_bags, "no shopping bag to remove"
        delete(ShoppingBag, shop_id=shop.shop_id)
        self.shopping_bags.pop(shop)

    def remove_shopping_bags(self, shops):
        for shop in shops:
            self.remove_shopping_bag(shop)
            delete(ShoppingBag, shop_id=shop.shop_id)
        return True

    def calculate_price(self):
        total = 0
        for shop, bag in self.shopping_bags.items():
            total += bag.calculate_price()
        return total

    @staticmethod
    def _purchase_shopping_bag(username: str, bag: ShoppingBag, payment_details, purchased_shops: list,
                               delivery_details: dict):
        transaction = bag.purchase_bag(username, payment_details, delivery_details)
        purchased_shops.append(bag.shop)
        return transaction

    def purchase_cart(self, username: str, payment_details: dict, delivery_details: dict,
                      do_what_you_can: bool = False) -> List[Transaction]:
        purchased_shops = []
        actions = [
            Action(self._purchase_shopping_bag, username, bag, payment_details, purchased_shops, delivery_details)
            .set_reverse(Action(ShoppingBag.cancel_transaction), use_return_value=True)
            .set_error_message(f"failed to purchase shopping bag for shop {shop.name}")
            for shop, bag in self
        ]
        actions += [Action(self.remove_shopping_bags, purchased_shops)]
        actions = ActionPool(actions)
        assert actions.execute_actions(do_what_you_can)
        return actions.get_return_values()[:-1]

    def change_product_purchase_type(self, shop, product_id: int, purchase_type_id: int, pt_args: dict) -> bool:
        product = shop.products[product_id]
        return self.shopping_bags[shop].change_product_purchase_type(product, purchase_type_id, pt_args)
