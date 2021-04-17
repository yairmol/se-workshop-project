from __future__ import annotations
import threading
from datetime import datetime
from typing import List

from domain.commerce_system.appointment import Appointment
from domain.commerce_system.permission import Permission
from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.shop import Shop
from domain.commerce_system.transactionDTO import TransactionDTO, CartTransactionDTO
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

    def register(self, username: str, password: str, **user_details):
        return self.user_state.register(username, password)

    def logout(self):
        raise NotImplementedError()

    def buy_product(self, shop: Shop, product: Product, amount_to_buy: int, payment_details: dict) -> bool:
        product_dto = ProductDTO(product, amount_to_buy)
        bag = {product: amount_to_buy}
        # shop_product = {shop: product_dto}
        transaction = TransactionDTO(shop, product_dto, payment_details, datetime.now(), product.price)
        shop.add_transaction(bag, transaction)
        self.add_transaction(transaction)

    def buy_shopping_bag(self, shop: Shop, payment_details: dict) -> bool:
        bag = self.cart[shop]
        dto_products = self.products_to_dto(bag)
        # shop_products = {shop: dto_products}
        transaction = TransactionDTO(shop, dto_products, payment_details, datetime.now(), bag.calculate_price())
        if shop.add_transaction(bag, transaction):
            self.add_transaction(transaction)
            self.cart.remove_shopping_bag(shop)
            return True
        return False

    def buy_cart(self, payment_details: dict, all_or_nothing: bool) -> bool:
        if not all_or_nothing:
            for shop in self.cart:
                self.buy_shopping_bag(shop, payment_details)
        else:
            date = datetime.now()
            to_be_canceled = []
            check_if_canceled = False
            for shop, bag in self.cart:
                products_dto = self.products_in_bag_to_dto(bag)
                transaction = TransactionDTO(shop, products_dto, payment_details, date, bag.calculate_price)
                if not shop.add_transaction(bag, transaction):
                    self.cancel_orders(to_be_canceled)
                    check_if_canceled = True
                    break
                else:
                    self.add_transaction(transaction)
                    to_be_canceled += [transaction]
            if not check_if_canceled:
                self.cart.remove_all_shopping_bags()


    def add_transaction(self, transaction: TransactionDTO):
        raise NotImplementedError()

    def remove_transaction(self, transaction: TransactionDTO):
        raise NotImplementedError()

    def cancel_orders(self, to_be_canceled: list[TransactionDTO]):
        for transaction in to_be_canceled:
            self.remove_transaction(transaction)
            transaction.shop.remove_transaction(self.cart[transaction.shop], transaction)

    def products_in_bag_to_dto(self, bag):
        dto_list = []
        for product, amount in bag:
            dto_list += [ProductDTO(product, amount)]
        return dto_list

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
    def register(self, username: str, password: str, **user_details):
        raise Exception("Error: Logged-in User cannot register")


class Guest(UserState):

    def register(self, username: str, password: str, **user_details):
        return Subscribed(username, password)


class Subscribed(UserState):

    def __init__(self, user_name: str, password: str, **user_details):  # TO add relevant fields
        self.user_name = user_name
        self.password = password


class AppointmentState:
    pass
