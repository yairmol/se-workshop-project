from __future__ import annotations
import threading
from datetime import datetime
from typing import List

from domain.commerce_system.appointments import Appointment
from domain.commerce_system.permission import Permission
from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.shop import Shop
from domain.commerce_system.transactionDTO import TransactionDTO
from domain.commerce_system.utils import Transaction
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag


class User:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):  # TO add relevant fields to the user object
        self.user_state = Guest()

        self.counter_lock.acquire()
        self.id = self.__id_counter
        User.__id_counter = User.__id_counter + 1
        self.counter_lock.release()
        self.cart = ShoppingCart(self.id)

    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError()

    def register(self, username: str, email: str, password: str, **user_details) -> bool:
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def buy_product(self, shop: Shop, product: Product, payment_details: dict) -> bool:
        date = datetime.now()
        product_dto = ProductDTO(product)
        shop_product = {shop: product_dto}
        transaction = TransactionDTO(shop_product, payment_details, date, product.price)
        shop.add_transaction(transaction)

    def buy_shopping_bag(self, shop: Shop, payment_details: dict):
        date = datetime.now()
        bag = self.cart[shop]
        products = []
        for product in bag.products:
            products += ProductDTO(product)
        shop_products = {shop: products}
        transaction = TransactionDTO(shop_products, payment_details, date, bag.calculate_price())
        shop.add_transaction(transaction)

    def buy_cart(self, payment_details: dict) -> bool:
        date = datetime.now()
        shops_products = {}
        for shop, bag in self.cart:
            products = []
            for product in bag.products:
                products += ProductDTO(product)
            shops_products[shop] = products
        transaction = TransactionDTO(shops_products, payment_details, date, self.cart.calculate_price())
        shop.add_transaction(transaction)

    def save_product_to_cart(self, shop: Shop, product: Product, quantity: int) -> bool:
        return self.cart.add_product(product, shop, quantity)

    def get_cart_info(self) -> List[dict]:
        raise NotImplementedError()

    def open_shop(self, **shop_details) -> Shop:
        raise NotImplementedError()

    def get_personal_transactions_history(self) -> List[Transaction]:
        raise NotImplementedError()

    def add_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def edit_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def delete_product(self, shop: Shop, product_id: str) -> Product:
        raise NotImplementedError()

    def appoint_shop_owner(self, shop: Shop, user) -> Appointment:
        raise NotImplementedError()

    def appoint_shop_manager(self, shop: Shop, user, permissions: List[Permission]) -> bool:
        raise NotImplementedError()

    def unappoint_shop_worker(self, shop: Shop, user) -> bool:
        raise NotImplementedError()

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        raise NotImplementedError()

    def get_shop_transaction_history(self, shop: Shop) -> List[Transaction]:
        raise NotImplementedError()

    def set_user_state(self, user_state: UserState):
        self.user_state = user_state


class UserState:
    pass


class Guest(UserState):
    pass


class Subscribed(UserState):

    def __init__(self, user_name: str):  # TO add relevant fields
        self.user_name = user_name


class AppointmentState:
    pass
