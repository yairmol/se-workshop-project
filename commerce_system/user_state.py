from typing import List

from commerce_system.appointments import Appointment
from commerce_system.permission import Permission
from commerce_system.shop import Shop
from commerce_system.utils import Transaction


class UserState:
    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError()

    def register(self, username: str, email: str, password: str, **user_details) -> bool:
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def buy_product(self, shop: Shop, product_id: str, payment_details: dict) -> bool:
        raise NotImplementedError()

    def buy_shopping_bag(self, shop: Shop, payment_details: dict):
        raise NotImplementedError()

    def buy_cart(self, payment_details: dict) -> bool:
        raise NotImplementedError()

    def save_product_to_cart(self, shop: Shop, product_id: str) -> bool:
        raise NotImplementedError()

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


class Guest(UserState):
    pass


class Subscribed(UserState):
    pass


class AppointmentState:
    pass
