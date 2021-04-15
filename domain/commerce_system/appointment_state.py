from typing import List

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User


class AppointmentState:
    pass


class ShopManager(AppointmentState):
    def __init__(self, shop: Shop):
        self.shop = shop


class ShopOwner(AppointmentState):
    shop = None

    def __init__(self, shop: Shop):
        self.shop = shop

    """ adds shop appointment of choice to selected subscribed user"""
    def add_appointment(self, appointment: AppointmentState, sub):
        apps = sub.appointments
        if self.shop in apps.keys():
            raise Exception("subscriber already has appointment for shop. shop id - ", self.shop.shop_id)
        apps[self.shop] = appointment

    """ removes shop appointment from selected subscribed user"""
    def remove_appointment(self, sub):
        sub.appointments.pop(self.shop)

    def add_product(self, product: Product) -> int:
        return self.shop.add_product(product)
    
    def edit_product(self, product_id: int, **to_edit):
        self.shop.edit_product(product_id, **to_edit)

    def delete_product(self, product_id: int):
        self.shop.delete_product(product_id)
    
    def appoint_manager(self, user: User):
        pass
    
    def appoint_owner(self, user: User):
        pass
    
    def edit_manager_perms(self, user: User, perms: List[str]):
        pass
    
    def un_appoint_manager(self, user: User):
        pass
    
    def get_shop_staff_info(self):
        pass
    
    def get_purchase_history(self):
        pass
