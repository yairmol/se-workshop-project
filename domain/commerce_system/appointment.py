from __future__ import annotations

import threading
from typing import List

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.logger.log import error_logger


class Appointment:

    def __init__(self, shop: Shop, username: str, appointer=None):
        self.username = username
        self.shop = shop
        self.appointer = appointer

    def appoint_manager(self, sub, permissions: List[str]):
        raise Exception("The Subscribed User doesn't have the permission to appoint manager")

    """ adds owner appointment to selected subscribed user"""

    def appoint_owner(self, sub):
        raise Exception("Subscribed user does not have permission to perform action")

    """ removes shop appointment from selected subscribed user"""

    def remove_appointment(self, sub):
        raise Exception("Subscribed user does not have permission to perform action")

    def add_product(self, **product_info) -> int:
        raise Exception("Subscribed user does not have permission to perform action")

    def edit_product(self, product_id: int, **to_edit):
        raise Exception("Subscribed user does not have permission to perform action")

    def delete_product(self, product_id: int) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_manager(self, manager_sub, cascading=False):
        raise Exception("Subscribed user does not have permission to perform action")

    def edit_manager_permissions(self, manager_sub, permissions: List[str]):
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_appointees(self):
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_owner(self, owner_sub, cascading=False):
        raise Exception("Subscribed user does not have permission to perform action")

    def edit_manager_perms(self, manager_sub, perms: List[str]):
        raise Exception("Subscribed user does not have permission to perform action")

    def get_shop_staff_info(self):
        raise Exception("Subscribed user does not have permission to perform action")

    def get_shop_transaction_history(self):
        raise Exception("Subscribed user does not have permission to perform action")


class ShopManager(Appointment):

    def __init__(self, shop: Shop, appointer: ShopOwner, permissions: List[str], username: str = "default_username"):
        super().__init__(shop, username, appointer)
        self.delete_product_permission = False
        self.edit_product_permission = False
        self.add_product_permission = False
        self.get_trans_history_permission = False
        self.set_permission(permissions)

    def add_product(self, **product_info) -> int:
        assert self.add_product_permission, "manager does not have permission to add product"
        product = Product(**product_info)
        return self.shop.add_product(product)

    def edit_product(self, product_id: int, **to_edit):
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        return self.shop.delete_product(product_id)

    def get_shop_transaction_history(self):
        assert self.get_trans_history_permission, "manager user does not have permission to perform the action"
        return self.shop.get_shop_transaction_history()

    def set_permission(self, permissions: List[str]):
        self.delete_product_permission = "delete_product" in permissions
        self.edit_product_permission = "edit_product" in permissions
        self.add_product_permission = "add_product" in permissions
        self.get_trans_history_permission = "get_transaction_history" in permissions


class ShopOwner(Appointment):
    def __init__(self, shop: Shop, username: str = "default_username", appointer=None):
        super().__init__(shop, username, appointer)
        self.owner_appointees = []
        self.manager_appointees = []
        self.manager_appointees_lock = threading.Lock()
        self.owner_appointees_lock = threading.Lock()

    """ adds manager appointment to selected subscribed user"""
    def appoint_manager(self, sub, permissions: List[str]):
        apps = sub.appointments
        assert self.shop not in apps.keys(), f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopManager(self.shop, self, permissions, sub.username)
        apps[self.shop] = appointment
        self.manager_appointees_lock.acquire()
        self.manager_appointees += [sub]
        self.manager_appointees_lock.release()
        self.shop.add_manager(sub)

    """ adds owner appointment to selected subscribed user"""
    def appoint_owner(self, sub):
        apps = sub.appointments
        assert self.shop not in apps.keys(), f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopOwner(self.shop, sub.username, self)
        apps[self.shop] = appointment
        self.owner_appointees_lock.acquire()
        self.owner_appointees += [sub]
        self.owner_appointees_lock.release()
        self.shop.add_owner(sub)

    """ removes shop appointment from selected subscribed user"""
    def remove_appointment(self, sub):
        sub.appointments.pop(self.shop)

    def add_product(self, **product_info) -> int:
        product = Product(**product_info)
        return self.shop.add_product(product)
    
    def edit_product(self, product_id: int, **to_edit):
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        return self.shop.delete_product(product_id)
    
    def un_appoint_manager(self, manager_sub, cascading=False):
        assert self.shop in manager_sub.appointments.keys() and isinstance(manager_sub.appointments[self.shop],
                                                                       ShopManager), "user is not a manager"
        assert manager_sub in self.manager_appointees, "manager was not assigned by this owner"
        self.remove_appointment(manager_sub)
        self.shop.remove_manager(manager_sub)
        if not cascading:
            self.manager_appointees_lock.acquire()
            self.manager_appointees.remove(manager_sub)
            self.manager_appointees_lock.release()

    def edit_manager_permissions(self, manager_sub, permissions: List[str]):
        assert self.shop in manager_sub.appointments.keys() and isinstance(manager_sub.appointments[self.shop],
                                                                       ShopManager), "user is not a manager"
        assert manager_sub in self.manager_appointees, "manager was not assigned by this owner"
        manager_sub.appointments[self.shop].set_permissions(permissions)

    def un_appoint_appointees(self):
        self.owner_appointees_lock.acquire()
        for owner in self.owner_appointees:
            self.un_appoint_owner(owner, cascading=True)
        self.owner_appointees_lock.release()
        self.manager_appointees_lock.acquire()
        for manager in self.manager_appointees:
            self.un_appoint_manager(manager, cascading=True)
        self.manager_appointees_lock.release()

    def un_appoint_owner(self, owner_sub, cascading=False):
        assert self.shop in owner_sub.appointments.keys() and isinstance(owner_sub.appointments[self.shop], ShopOwner), "user is not an owner"
        assert owner_sub in self.owner_appointees, "owner was not assigned by this owner"
        owner_sub.appointments[self.shop].un_appoint_appointees()
        self.remove_appointment(owner_sub)
        self.shop.remove_owner(owner_sub)
        if not cascading:
            self.owner_appointees_lock.acquire()
            self.owner_appointees.remove(owner_sub)
            self.owner_appointees_lock.release()

    def promote_manager_to_owner(self, manager_sub):
        self.un_appoint_manager(manager_sub)
        self.appoint_owner(manager_sub)

    def get_shop_transaction_history(self):
        return self.shop.get_shop_transaction_history()

    def get_shop_staff_info(self):
        pass
