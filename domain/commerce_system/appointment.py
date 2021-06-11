from __future__ import annotations

import threading
from typing import List, Dict

from data_access_layer.engine import add_to_session
from domain.commerce_system.product import Product, PurchaseType, PurchaseOffer
from domain.commerce_system.purchase_conditions import Policy
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.discount_module.discount_calculator import Discount
from data_model import AppointmentModel as Am, PermissionsModel as Perms


class Appointment:

    def __init__(self, shop: Shop, username: str, appointer_username=None):
        self.username = username
        self.shop = shop
        self.appointer_username = appointer_username

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def appoint_manager(self, sub, permissions: List[str]) -> Appointment:
        raise Exception("The Subscribed User doesn't have the permission to appoint manager")

    def appoint_owner(self, sub) -> Appointment:
        """ adds owner appointment to selected subscribed user"""
        raise Exception("Subscribed user does not have permission to perform action")

    def remove_appointment(self, sub) -> bool:
        """ removes shop appointment from selected subscribed user"""
        raise Exception("Subscribed user does not have permission to perform action")

    def add_product(self, **product_info) -> Product:
        raise Exception("Subscribed user does not have permission to perform action")

    def edit_product(self, product_id: int, **to_edit) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def delete_product(self, product_id: int) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_manager(self, manager_sub, cascading=False) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def edit_manager_permissions(self, manager_sub, permissions: List[str]) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_appointees(self) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def un_appoint_owner(self, owner_sub, cascading=False) -> bool:
        raise Exception("Subscribed user does not have permission to perform action")

    def get_shop_staff_info(self) -> List:
        raise Exception("Subscribed user does not have permission to perform action")

    def get_shop_transaction_history(self) -> List[Transaction]:
        raise Exception("Subscribed user does not have permission to perform action")

    def promote_manager_to_owner(self, manager_sub) -> Appointment:
        raise Exception("Cannot promote manager to owner")

    def get_discounts(self) -> List[Discount]:
        raise Exception("Cannot get discounts")

    def add_discount(self, has_cond: bool, condition, discount) -> Discount:
        raise Exception("Cannot manage discounts")

    def delete_discounts(self, discount_ids: List[int]) -> bool:
        raise Exception("Cannot manage discounts")

    def aggregate_discounts(self, discount_ids: List[int], func: str) -> bool:
        raise Exception("Cannot manage discounts")

    def move_discount_to(self, src_discount_id: int, dst_discount_id: int) -> bool:
        raise Exception("Cannot manage discounts")

    def get_purchase_conditions(self) -> List[Policy]:
        raise Exception("Cannot get purchase conditions")

    def add_purchase_condition(self, condition: Policy) -> bool:
        raise Exception("Cannot manage conditions")

    def remove_purchase_condition(self, condition_id: int) -> bool:
        raise Exception("Cannot manage conditions")

    def get_permissions(self) -> Dict[str, bool]:
        raise NotImplementedError()

    def add_purchase_type(self, product_id: int, purchase_type_info: dict) -> PurchaseType:
        raise Exception("Cannot manage purchase types")

    def reply_price_offer(self, product_id: int, offer_maker: str, action: str, **kwargs) -> bool:
        raise Exception("Cannot reply to price offer")

    def get_offers(self, product_id: int) -> List[PurchaseOffer]:
        raise NotImplementedError()


class ShopManager(Appointment):

    def __init__(self, shop: Shop, appointer_username: str, permissions: List[str], username: str = "default_username"):
        super().__init__(shop, username, appointer_username)
        self.purchase_type_permission = False
        self.delete_product_permission = False
        self.edit_product_permission = False
        self.add_product_permission = False
        self.discount_permission = False
        self.purchase_condition_permission = False
        self.get_trans_history_permission = False
        self.get_staff_permission = False
        self.set_permissions(permissions)

    def to_dict(self) -> dict:
        ret = {
            Am.WORKER_NAME: self.username,
            Am.WORKER_TITLE: "manager",
            Am.WORKER_APPOINTER: self.appointer_username,
            Am.PERMISSIONS: self.get_permissions()
        }
        ret.update(self.shop.to_dict(include_products=False))
        return ret

    def add_product(self, **product_info) -> Product:
        assert self.add_product_permission, "manager does not have permission to add product"
        return self.shop.add_product(**product_info)

    def edit_product(self, product_id: int, **to_edit) -> bool:
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        self.shop.edit_product(product_id, **to_edit)
        return True

    def delete_product(self, product_id: int) -> bool:
        assert self.edit_product_permission, "manager user does not have permission to perform the action"
        return self.shop.delete_product(product_id)

    def get_shop_transaction_history(self) -> List[Transaction]:
        assert self.get_trans_history_permission, "manager user does not have permission to perform the action"
        return self.shop.get_shop_transaction_history()

    def set_permissions(self, permissions: List[str]) -> None:
        self.delete_product_permission = Perms.DELETE_PRODUCT_PERM in permissions
        self.edit_product_permission = Perms.EDIT_PRODUCT_PERM in permissions
        self.add_product_permission = Perms.ADD_PRODUCT_PERM in permissions
        self.get_trans_history_permission = Perms.WATCH_TRANSACTIONS_PERM in permissions
        self.discount_permission = Perms.MANAGE_DISCOUNT_PERM in permissions
        self.get_staff_permission = Perms.WATCH_STAFF_PERM in permissions
        self.purchase_condition_permission = Perms.MANAGE_PURCHASE_CONDITIONS in permissions

    def get_discounts(self) -> List[Discount]:
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.get_discounts()

    def add_discount(self, has_cond, condition, discount) -> Discount:
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.add_discount(has_cond, condition, discount)

    def delete_discounts(self, discount_ids) -> bool:
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.delete_discounts(discount_ids)

    def aggregate_discounts(self, discount_ids: [int], func: str) -> bool:
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.aggregate_discounts(discount_ids, func)

    def move_discount_to(self, src_discount_id: int, dst_discount_id: int) -> bool:
        assert self.discount_permission, "manager user does not have permission to manage discounts"
        return self.shop.move_discount_to(src_discount_id, dst_discount_id)

    def get_purchase_conditions(self):
        assert self.purchase_condition_permission, "manager user does not have permission to manage purchase conditions"
        return self.shop.get_purchase_conditions()

    def add_purchase_condition(self, condition: Policy) -> bool:
        assert self.purchase_condition_permission, "manager user does not have permission to" \
                                                   " manage purchase conditions"
        return self.shop.add_purchase_condition(condition)

    def remove_purchase_condition(self, condition_id: int) -> bool:
        assert self.purchase_condition_permission, "manager user does not have permission to " \
                                                   "manage purchase conditions"
        return self.shop.remove_purchase_condition(condition_id)

    def get_permissions(self):
        return {
            Perms.ADD_PRODUCT_PERM: self.add_product_permission,
            Perms.EDIT_PRODUCT_PERM: self.edit_product_permission,
            Perms.DELETE_PRODUCT_PERM: self.delete_product_permission,
            Perms.MANAGE_DISCOUNT_PERM: self.discount_permission,
            Perms.WATCH_TRANSACTIONS_PERM: self.get_trans_history_permission,
            Perms.WATCH_STAFF_PERM: self.get_staff_permission,
            Perms.MANAGE_PURCHASE_CONDITIONS: self.purchase_condition_permission,
            Perms.PURCHASE_TYPES_PERM: self.purchase_condition_permission,
            'owner': False
        }

    def get_shop_staff_info(self) -> List:
        assert self.get_staff_permission, "manager user does not have permission to see shop staff"
        return self.shop.get_staff_info()

    def add_purchase_type(self, product_id: int, purchase_type_info: dict) -> PurchaseType:
        assert self.purchase_type_permission, "manager user does not have permission to manage purchase types"
        return self.shop.add_purchase_type(product_id, purchase_type_info)

    def reply_price_offer(self, product_id: int, offer_maker: str, action: str, **kwargs) -> bool:
        assert self.purchase_type_permission, "manager user does not have permission to manage purchase types"
        return self.shop.reply_price_offer(product_id, offer_maker, action, action_maker=self.username, **kwargs)

    def get_offers(self, product_id: int) -> List[PurchaseOffer]:
        assert self.purchase_type_permission, "manager user does not have permission to manage purchase types"
        return self.shop.products[product_id].get_offers()


class ShopOwner(Appointment):
    def __init__(self, shop: Shop, username: str = "default_username", appointer_username=None):
        super().__init__(shop, username, appointer_username)
        self.appointees = []
        self.appointees_lock = threading.Lock()

    # @add_to_session
    def get_appointees(self):
        return self.appointees

    def to_dict(self):
        ret = {
            Am.WORKER_NAME: self.username,
            Am.WORKER_TITLE: "owner" if self != self.shop.founder else "founder",
            Am.WORKER_APPOINTER: self.appointer_username if self.appointer_username else "no appointer, this is the shop founder"
        }
        ret.update(self.shop.to_dict(include_products=False))
        return ret

    def appoint_manager(self, sub, permissions: List[str]) -> Appointment:
        """ adds manager appointment to selected subscribed user"""
        apps = sub.appointments
        assert self.shop not in apps.keys(), \
            f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopManager(self.shop, self.username, permissions, sub.username)
        apps[self.shop] = appointment
        with self.appointees_lock:
            self.appointees += [sub]
        self.shop.add_manager(appointment)
        return appointment

    def appoint_owner(self, new_owner_sub) -> Appointment:
        """ adds owner appointment to selected subscribed user"""
        apps = new_owner_sub.appointments
        assert self.shop not in apps, f"subscriber already has appointment for shop. shop id - {self.shop.shop_id}"
        appointment = ShopOwner(self.shop, new_owner_sub.username, self)
        apps[self.shop] = appointment
        with self.appointees_lock:
            self.appointees += [new_owner_sub]
        self.shop.add_owner(appointment)
        return appointment

    def remove_appointment(self, sub) -> bool:
        """ removes shop appointment from selected subscribed user"""
        sub.appointments.pop(self.shop)
        return True

    def add_product(self, **product_info) -> Product:
        return self.shop.add_product(**product_info)

    def edit_product(self, product_id: int, **to_edit) -> bool:
        return self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int) -> bool:
        return self.shop.delete_product(product_id)

    def un_appoint_manager(self, manager_sub, cascading=False) -> bool:
        assert self.shop in manager_sub.appointments and isinstance(manager_sub.appointments[self.shop], ShopManager), \
            "user is not a manager"
        assert manager_sub in self.appointees, "manager was not assigned by this owner"
        success = True
        success = success and self.remove_appointment(manager_sub)
        success = success and self.shop.remove_manager(manager_sub)
        if not cascading:
            with self.appointees_lock:
                self.appointees.remove(manager_sub)
        return success

    def edit_manager_permissions(self, manager_sub, permissions: List[str]) -> bool:
        assert self.shop in manager_sub.appointments.keys() \
               and isinstance(manager_sub.appointments[self.shop], ShopManager), "user is not a manager"
        assert manager_sub in self.appointees, "manager was not assigned by this owner"
        manager_sub.appointments[self.shop].set_permissions(permissions)
        return True

    def un_appoint_appointees(self) -> bool:
        success = True
        with self.appointees_lock:
            for sub in self.appointees:
                if isinstance(sub.appointments[self.shop], ShopOwner):
                    success = success and self.un_appoint_owner(sub, cascading=True)
                else:
                    success = success and self.un_appoint_manager(sub, cascading=True)
        return success

    def un_appoint_owner(self, owner_sub, cascading=False) -> bool:
        assert (self.shop in owner_sub.appointments.keys()
                and isinstance(owner_sub.appointments[self.shop], ShopOwner)), "user is not an owner"
        assert owner_sub in self.appointees, "owner was not assigned by this owner"
        success = True
        success = success and owner_sub.appointments[self.shop].un_appoint_appointees()
        success = success and self.remove_appointment(owner_sub)
        success = success and self.shop.remove_owner(owner_sub)
        if not cascading:
            with self.appointees_lock:
                self.appointees.remove(owner_sub)
        return success

    def promote_manager_to_owner(self, manager_sub) -> Appointment:
        self.un_appoint_manager(manager_sub)
        return self.appoint_owner(manager_sub)

    def get_shop_transaction_history(self) -> List[Transaction]:
        return self.shop.get_shop_transaction_history()

    def get_shop_staff_info(self) -> List:
        return self.shop.get_staff_info()

    def get_discounts(self) -> List[Discount]:
        return self.shop.get_discounts()

    def add_discount(self, has_cond, condition, discount) -> Discount:
        return self.shop.add_discount(has_cond, condition, discount)

    def delete_discounts(self, discount_ids) -> bool:
        return self.shop.delete_discounts(discount_ids)

    def aggregate_discounts(self, discount_ids, func) -> bool:
        return self.shop.aggregate_discounts(discount_ids, func)

    def move_discount_to(self, src_discount_id, dst_discount_id) -> bool:
        return self.shop.move_discount_to(src_discount_id, dst_discount_id)

    def get_purchase_conditions(self):
        return self.shop.get_purchase_conditions()

    def add_purchase_condition(self, condition: Policy) -> bool:
        return self.shop.add_purchase_condition(condition)

    def remove_purchase_condition(self, condition_id: int) -> bool:
        return self.shop.remove_purchase_condition(condition_id)

    def get_permissions(self):
        ret = {
            Perms.ADD_PRODUCT_PERM: True,
            Perms.EDIT_PRODUCT_PERM: True,
            Perms.DELETE_PRODUCT_PERM: True,
            Perms.MANAGE_DISCOUNT_PERM: True,
            Perms.WATCH_TRANSACTIONS_PERM: True,
            Perms.WATCH_STAFF_PERM: True,
            Perms.MANAGE_PURCHASE_CONDITIONS: True,
            'owner': True
        }
        return ret

    def add_purchase_type(self, product_id: int, purchase_type_info: dict) -> PurchaseType:
        return self.shop.add_purchase_type(product_id, purchase_type_info)

    def reply_price_offer(self, product_id: int, offer_maker: str, action: str, **kwargs) -> bool:
        return self.shop.reply_price_offer(product_id, offer_maker, action, action_maker=self.username, **kwargs)

    def get_offers(self, product_id: int) -> List[PurchaseOffer]:
        return self.shop.products[product_id].get_offers()
