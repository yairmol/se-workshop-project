from __future__ import annotations

import threading
from typing import List

from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import Condition
from domain.commerce_system.shop import Shop


class Appointment:

    def __init__(self, shop: Shop, username: str, appointer=None):
        self.username = username
        self.shop = shop
        self.appointer = appointer

    def appoint_manager(self, sub, permissions: List[str]):
        raise Exception("The Subscribed User doesn't have the permission to appoint manager")

    def appoint_owner(self, sub):
        """ adds owner appointment to selected subscribed user"""
        raise Exception("Subscribed user does not have permission to perform action")

    def remove_appointment(self, sub):
        """ removes shop appointment from selected subscribed user"""
        raise Exception("Subscribed user does not have permission to perform action")

    def add_product(self, **product_info) -> Product:
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

    def promote_manager_to_owner(self, manager_sub):
        raise Exception("Cannot promote manager to owner")

    def add_discount(self, has_cond, condition, discount):
        raise Exception("Cannot manage discounts")

    def delete_discount(self, discount_ids):
        raise Exception("Cannot manage discounts")

    def aggregate_discounts(self, discount_ids, func):
        raise Exception("Cannot manage discounts")

    def add_purchase_condition(self, condition: Condition):
        raise Exception("Cannot manage conditions")

    def remove_purchase_condition(self, condition_id: int):
        raise Exception("Cannot manage conditions")

    def get_permissions(self):
        pass


class ShopManager(Appointment):

    def __init__(self, shop: Shop, appointer: ShopOwner, permissions: List[str], username: str = "default_username"):
        super().__init__(shop, username, appointer)
        self.delete_product_permission = False
        self.edit_product_permission = False
        self.add_product_permission = False
        self.discount_permission = False
        self.purchase_condition_permission = False
        self.get_trans_history_permission = False
        self.set_permissions(permissions)

    def add_product(self, **product_info) -> Product:
        assert self.add_product_permission, "manager does not have permission to add product"
        return self.shop.add_product(**product_info)

    def edit_product(self, product_id: int, **to_edit):
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        return self.shop.delete_product(product_id)

    def get_shop_transaction_history(self):
        assert self.get_trans_history_permission, "manager user does not have permission to perform the action"
        return self.shop.get_shop_transaction_history()

    def set_permissions(self, permissions: List[str]):
        self.delete_product_permission = "delete_product" in permissions
        self.edit_product_permission = "edit_product" in permissions
        self.add_product_permission = "add_product" in permissions
        self.get_trans_history_permission = "get_transaction_history" in permissions
        self.get_trans_history_permission = "discount" in permissions

    def add_discount(self, has_cond, condition, discount):
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.add_discount(has_cond, condition, discount)

    def delete_discounts(self, discount_ids):
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.delete_discounts(discount_ids)

    def aggregate_discounts(self, discount_ids: [int], func: str):
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.aggregate_discounts(discount_ids, func)

    def add_purchase_condition(self, condition: Condition):
        assert self.purchase_condition_permission, "manager user does not have permission to" \
                                                   " manage purchase conditions"
        return self.shop.add_purchase_condition(condition)

    def remove_purchase_condition(self, condition_id: int):
        assert self.purchase_condition_permission, "manager user does not have permission to " \
                                                   "manage purchase conditions"
        assert self.shop.remove_purchase_condition(condition_id), "remove condition failed"

    def get_permissions(self):
        return {'delete': self.delete_product_permission, 'edit': self.edit_product_permission,
                'add': self.add_product_permission, 'discount': self.discount_permission,
                'transaction': self.get_trans_history_permission, 'owner': False}


class ShopOwner(Appointment):
    def __init__(self, shop: Shop, username: str = "default_username", appointer=None):
        super().__init__(shop, username, appointer)
        self.owner_appointees = []
        self.manager_appointees = []
        self.manager_appointees_lock = threading.Lock()
        self.owner_appointees_lock = threading.Lock()

    def appoint_manager(self, sub, permissions: List[str]):
        """ adds manager appointment to selected subscribed user"""
        apps = sub.appointments
        assert self.shop not in apps.keys(), \
            f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopManager(self.shop, self, permissions, sub.username)
        apps[self.shop] = appointment
        self.manager_appointees_lock.acquire()
        self.manager_appointees += [sub]
        self.manager_appointees_lock.release()
        self.shop.add_manager(sub)

    def appoint_owner(self, new_owner_sub):
        """ adds owner appointment to selected subscribed user"""
        apps = new_owner_sub.appointments
        assert self.shop not in apps, f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopOwner(self.shop, new_owner_sub.username, self)
        apps[self.shop] = appointment
        self.owner_appointees_lock.acquire()
        self.owner_appointees += [new_owner_sub]
        self.owner_appointees_lock.release()
        self.shop.add_owner(new_owner_sub)

    def remove_appointment(self, sub):
        """ removes shop appointment from selected subscribed user"""
        sub.appointments.pop(self.shop)

    def add_product(self, **product_info) -> Product:
        return self.shop.add_product(**product_info)

    def edit_product(self, product_id: int, **to_edit):
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        return self.shop.delete_product(product_id)

    def un_appoint_manager(self, manager_sub, cascading=False):
        assert self.shop in manager_sub.appointments and isinstance(manager_sub.appointments[self.shop], ShopManager), \
            "user is not a manager"
        assert manager_sub in self.manager_appointees, "manager was not assigned by this owner"
        self.remove_appointment(manager_sub)
        self.shop.remove_manager(manager_sub)
        if not cascading:
            self.manager_appointees_lock.acquire()
            self.manager_appointees.remove(manager_sub)
            self.manager_appointees_lock.release()

    def edit_manager_permissions(self, manager_sub, permissions: List[str]):
        assert self.shop in manager_sub.appointments.keys() \
               and isinstance(manager_sub.appointments[self.shop], ShopManager), "user is not a manager"
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
        assert self.shop in owner_sub.appointments.keys() and isinstance(owner_sub.appointments[self.shop], ShopOwner), \
            "user is not an owner"
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

    def add_discount(self, has_cond, condition, discount):
        return self.shop.add_discount(has_cond, condition, discount)

    def delete_discounts(self, discount_ids):
        return self.shop.delete_discounts(discount_ids)

    def aggregate_discounts(self, discount_ids, func):
        return self.shop.aggregate_discounts(discount_ids, func)

    def add_purchase_condition(self, condition: Condition):
        return self.shop.add_purchase_condition(condition)

    def remove_purchase_condition(self, condition_id: int):
        assert self.shop.remove_purchase_condition(condition_id), "remove condition failed"

    def get_permissions(self):
        return {'delete': True, 'edit': True, 'add': True, 'discount': True, 'transaction': True, 'owner': True}