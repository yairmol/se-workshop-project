from __future__ import annotations

from typing import List

from domain.commerce_system.appointment import Appointment, ShopOwner
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import UserState


class Subscribed(UserState):
    appointments = None

    def __init__(self, username: str, password: str):
        self.appointments = {}
        self.username = username
        self.password = password

    def open_store(self, store_credentials: dict) -> bool:
        raise NotImplementedError()

    def get_transaction_history(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    """ calls personal appointment for the request. if doesnt have permission raises an exception"""
    def appoint_manager(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_manager(self, permissions)

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_owner(self)

    def get_appointment(self, shop: Shop):
        try:
            return self.appointments[shop]
        except Exception as e:
            raise Exception("no appointment for shop. shop id - ", shop.shop_id)

    def add_product(self, shop: Shop, product: Product) -> int:
        return self.get_appointment(shop).add_product(product)

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

