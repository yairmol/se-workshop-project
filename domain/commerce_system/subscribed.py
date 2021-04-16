from __future__ import annotations

from domain.commerce_system.appointment import Appointment, ShopOwner
from domain.commerce_system.shop import Shop
from domain.commerce_system.user_state import UserState


class Subscribed:
    appointments = None

    def __init__(self, username: str):
        self.appointments = {}
        self.username = username

    def open_store(self, store_credentials: dict) -> bool:
        raise NotImplementedError()

    def get_transaction_history(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    """ calls personal appointment for the request. if doesnt have permission raises an exception"""
    def appoint_manager(self, owner_sub: Subscribed, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_manager(self)

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.appoint_owner(self)

    def get_appointment(self, shop: Shop):
        try:
            return self.appointments[shop]
        except Exception as e:
            raise Exception("no appointment for shop. shop id - ", shop.shop_id)

    def un_appoint_manager(self, owner_sub, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.un_appoint_manager(self)

    def un_appoint_owner(self, owner_sub, shop: Shop):
        session_app = owner_sub.get_appointment(shop)
        session_app.un_appoint_owner(self)


