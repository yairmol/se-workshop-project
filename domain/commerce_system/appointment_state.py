from typing import List

from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User


class AppointmentState:
    pass


class ShopManager(AppointmentState):
    pass


class ShopOwner(AppointmentState):
    def __init__(self):
        pass

    def add_product(self, shop: Shop, product: Product, quantity: int) -> int:
        return shop.add_product(product, quantity)
    
    def edit_product(self, shop: Shop, product_id: int, **to_edit) -> bool:
        return shop.edit_product(product_id, **to_edit)

    def delete_product(self, shop: Shop, product_id: int) -> bool:
        return shop.delete_product(product_id)
    
    def appoint_manager(self, shop: Shop, user: User):
        pass
    
    def appoint_owner(self, shop: Shop, user: User):
        pass
    
    def edit_manager_perms(self, shop: Shop, user: User, perms: List[str]):
        pass
    
    def un_appoint_manager(self, shop: Shop, user: User):
        pass
    
    def get_shop_staff_info(self, shop: Shop):
        pass
    
    def get_purchase_history(self, shop: Shop):
        pass
