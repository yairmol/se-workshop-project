from __future__ import annotations
from typing import List

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop


class Appointment:
    appointer: ShopOwner = None
    shop: Shop = None

    def __init__(self, shop: Shop, appointer=None):
        self.shop = shop
        self.appointer = appointer


class ShopManager(Appointment):
    def __init__(self, shop: Shop, appointer: ShopOwner):
        super().__init__(shop, appointer)


class ShopOwner(Appointment):
    def __init__(self, shop: Shop, appointer=None):
        super().__init__(shop, appointer)
        self.owner_appointees = []
        self.manager_appointees = []

    """ adds manager appointment to selected subscribed user"""
    def appoint_manager(self, sub):
        appointment = ShopManager(self.shop, self)
        apps = sub.appointments
        if self.shop in apps.keys():
            raise Exception("subscriber already has appointment for shop. shop id - ", self.shop.shop_id)
        apps[self.shop] = appointment
        self.manager_appointees += [sub]

    """ adds owner appointment to selected subscribed user"""
    def appoint_owner(self, sub):
        appointment = ShopOwner(self.shop, self)
        apps = sub.appointments
        if self.shop in apps.keys():
            raise Exception("subscriber already has appointment for shop. shop id - ", self.shop.shop_id)
        apps[self.shop] = appointment
        self.owner_appointees += [sub]

    """ removes shop appointment from selected subscribed user"""
    def remove_appointment(self, sub):
        sub.appointments.pop(self.shop)

    def add_product(self, product: Product) -> int:
        return self.shop.add_product(product)
    
    def edit_product(self, product_id: int, **to_edit):
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        self.shop.delete_product(product_id)
    
    def edit_manager_perms(self, manager_sub, perms: List[str]):
        pass
    
    def un_appoint_manager(self, manager_sub, cascading=False):
        if self.shop in manager_sub.appointments.keys() and isinstance(manager_sub.appointments[self.shop],
                                                                       ShopManager):
            if manager_sub in self.manager_appointees:
                self.remove_appointment(manager_sub)
                if not cascading:
                    self.manager_appointees.remove(manager_sub)
            else:
                raise Exception("manager was not assigned by this owner")
        else:
            raise Exception("user is not a manager")

    def un_appoint_appointees(self):
        for owner in self.owner_appointees:
            self.un_appoint_owner(owner, cascading=True)
        for manager in self.manager_appointees:
            self.un_appoint_manager(manager, cascading=True)

    def un_appoint_owner(self, owner_sub, cascading=False):
        if self.shop in owner_sub.appointments.keys() and isinstance(owner_sub.appointments[self.shop], ShopOwner):
            if owner_sub in self.owner_appointees:
                owner_sub.appointments[self.shop].un_appoint_appointees()
                self.remove_appointment(owner_sub)
                if not cascading:
                    self.owner_appointees.remove(owner_sub)
            else:
                raise Exception("owner was not assigned by this owner")
        else:
            raise Exception("user is not an owner")

    def get_shop_staff_info(self):
        pass
    
    def get_purchase_history(self):
        pass
