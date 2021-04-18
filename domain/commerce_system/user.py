from __future__ import annotations
import threading
from datetime import datetime
from typing import List, Dict

from domain.commerce_system.appointment import Appointment, ShopOwner
from domain.commerce_system.permission import Permission
from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.payment_module.payment_system import pay
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.shopping_cart import ShoppingCart


class User:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):
        self.user_state: UserState = Guest()
        self.counter_lock.acquire()
        self.id = self.__id_counter
        User.__id_counter = User.__id_counter + 1
        self.counter_lock.release()
        self.cart = ShoppingCart(self.id)

    def login(self, sub_user: Subscribed):
        self.user_state = sub_user

    def register(self, username: str, password: str, **user_details):
        return self.user_state.register(username, password)

    def logout(self):
        raise NotImplementedError()

    def buy_product(self, shop: Shop, product: Product, amount_to_buy: int, payment_details: dict):
        product_dto = ProductDTO(product, amount_to_buy)
        bag = {product: amount_to_buy}
        transaction = Transaction(shop, [product_dto], payment_details, datetime.now(), product.price)
        shop.add_transaction(bag, transaction)
        self.add_transaction(transaction)
        pay(self, payment_details)

    def buy_shopping_bag(self, shop: Shop, payment_details: dict) -> bool:
        bag = self.cart[shop]
        products_dtos = bag.get_products_dtos()
        transaction = Transaction(shop, products_dtos, payment_details, datetime.now(), bag.calculate_price())
        if shop.add_transaction(bag, transaction):
            self.add_transaction(transaction)
            self.cart.remove_shopping_bag(shop)
            pay(self, payment_details)
            return True
        return False

    def buy_cart(self, payment_details: dict, all_or_nothing: bool):
        if not all_or_nothing:
            for shop in self.cart:
                self.buy_shopping_bag(shop, payment_details)
        else:
            date = datetime.now()
            to_be_canceled = []
            check_if_canceled = False
            for shop, bag in self.cart:
                products_dto = bag.get_products_dtos()
                transaction = Transaction(shop, products_dto, payment_details, date, bag.calculate_price)
                if not shop.add_transaction(bag, transaction):
                    self.cancel_orders(to_be_canceled)
                    check_if_canceled = True
                    break
                else:
                    self.add_transaction(transaction)
                    to_be_canceled += [transaction]
            if not check_if_canceled:
                self.cart.remove_all_shopping_bags()
                pay(self, payment_details)

    def add_transaction(self, transaction: Transaction):
        self.user_state.add_transaction(transaction)

    def remove_transaction(self, transaction: Transaction):
        self.user_state.remove_transaction(transaction)

    def cancel_orders(self, to_be_canceled: list[Transaction]):
        for transaction in to_be_canceled:
            self.remove_transaction(transaction)
            transaction.shop.remove_transaction(self.cart[transaction.shop], transaction)

    def save_product_to_cart(self, shop: Shop, product: Product, amount_to_buy: int) -> bool:
        return self.cart.add_product(product, shop, amount_to_buy)

    def remove_product_from_cart(self, shop: Shop, product: Product, amount: int) -> bool:
        return self.cart.remove_from_shopping_bag(shop, product, amount)

    def get_cart_info(self) -> dict:
        return self.cart.to_dict()

    def open_shop(self, **shop_details) -> Shop:
        raise NotImplementedError()

    def get_personal_transactions_history(self) -> List[Transaction]:
        return self.user_state.get_personal_transaction_history()

    def add_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def edit_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def delete_product(self, shop: Shop, product_id: str) -> Product:
        raise NotImplementedError()

    def appoint_shop_owner(self, shop: Shop, user) -> Appointment:
        raise NotImplementedError()

    def appoint_shop_manager(self, shop: Shop, user, permissions: List[str]) -> bool:
        raise NotImplementedError()

    def unappoint_shop_worker(self, shop: Shop, user) -> bool:
        raise NotImplementedError()

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        raise NotImplementedError()

    def get_shop_transaction_history(self, shop: Shop) -> List[Transaction]:
        raise NotImplementedError()


class UserState:
    def register(self, username: str, password: str, **user_details):
        raise Exception("Error: Logged-in User cannot register")

    def appoint_manager(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        raise Exception("Error: Guest User cannot appoint manager")

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop):
        raise Exception("Error: Guest User cannot appoint owner")

    def get_appointment(self, shop: Shop):
        raise Exception("Error: Guest User cannot get appointment")

    def add_product(self, shop: Shop, **product_info) -> int:
        raise Exception("Error: Guest User cannot add product")

    def edit_product(self, shop: Shop, product_id: int, **to_edit):
        raise Exception("Error: Guest User cannot edit product")

    def delete_product(self, shop: Shop, product_id: int) -> bool:
        raise Exception("Error: Guest User cannot delete product")

    def un_appoint_manager(self, owner_sub, shop: Shop):
        raise Exception("Error: Guest User cannot un appoint manager")

    def un_appoint_owner(self, owner_sub, shop: Shop):
        raise Exception("Error: Guest User cannot un appoint owner")

    def edit_manager_permissions(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        raise Exception("Error: Guest User cannot edit manager permissions")

    def get_personal_transaction_history(self):
        raise Exception("Error: User cannot perform this action")

    def open_shop(self, shop_details):
        raise Exception("Error: Guest User cannot edit manager permissions")

    def add_transaction(self, transaction: Transaction):
        pass

    def remove_transaction(self, transaction: Transaction):
        psas


class Guest(UserState):

    def register(self, username: str, password: str, **user_details):
        return Subscribed(username, password)


class Subscribed(UserState):

    def __init__(self, username: str, password: str):
        self.appointments: Dict[Shop, Appointment] = {}
        self.username = username
        self.password = password
        self.transactions: List[Transaction] = []

    def logout(self):
        raise NotImplementedError()

    """ calls personal appointment for the request. if doesnt have permission raises an exception"""

    def appoint_manager(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_manager(self, permissions)

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_owner(self)

    def promote_manager_to_owner(self, owner_sub: Subscribed, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.promote_manager_to_owner(self)

    def get_appointment(self, shop: Shop):
        if shop in self.appointments:
            return self.appointments[shop]
        raise Exception("no appointment for shop. shop id - ", shop.shop_id)

    def add_product(self, shop: Shop, **product_info) -> int:
        return self.get_appointment(shop).add_product(**product_info)

    def edit_product(self, shop: Shop, product_id: int, **to_edit):
        self.get_appointment(shop).edit_product(product_id, **to_edit)

    def delete_product(self, shop: Shop, product_id: int):
        self.get_appointment(shop).delete_product(product_id)

    def un_appoint_manager(self, owner_sub, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.un_appoint_manager(self)

    def un_appoint_owner(self, owner_sub, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.un_appoint_owner(self)

    def edit_manager_permissions(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        session_app = owner_sub.get_appointment(shop)
        session_app.edit_manager_permissions(self, permissions)

    def open_shop(self, shop_details):
        new_shop = Shop(**shop_details)
        owner = ShopOwner(new_shop)
        self.appointments[new_shop] = owner
