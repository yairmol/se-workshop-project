from typing import List, Union

from commerce_system.facade import ICommerceSystemFacade


class CommerceSystemFacadeProxy(ICommerceSystemFacade):
    def __init__(self):
        self.real: Union[ICommerceSystemFacade, None] = None

    def enter(self) -> str:
        if self.real:
            return self.real.enter()
        return ""

    def exit(self, session_id: str) -> bool:
        if self.real:
            return self.real.exit(session_id)
        return False

    def register(self, session_id: str, username: str, password: str, email: str, **kwargs) -> bool:
        if self.real:
            return self.real.register(session_id, username, password, email, **kwargs)
        return False

    def login(self, session_id: str, username: str, password: str) -> bool:
        if self.real:
            return self.real.login(session_id, username, password)
        return False

    def logout(self, session_id: str) -> bool:
        if self.real:
            return self.real.logout(session_id)
        return False

    def get_shop_info(self, shop_id: str) -> dict:
        if self.real:
            return self.real.get_shop_info(shop_id)
        return {}

    def save_product_to_cart(self, session_id: str, shop_id: str, product_id: str) -> bool:
        if self.real:
            return self.real.save_product_to_cart(session_id, shop_id, product_id)
        return False

    def get_cart_info(self, session_id: str) -> dict:
        if self.real:
            return self.real.get_cart_info(session_id)
        return {}

    def search_products(self, keywords: str, filters: list) -> List[dict]:
        if self.real:
            return self.real.search_products(keywords, filters)
        return []

    def search_shops(self, keywords: str, filters: list) -> List[dict]:
        if self.real:
            return self.real.search_shops(keywords, filters)
        return []

    def purchase_cart(self, session_id: str) -> bool:
        if self.real:
            return self.real.purchase_cart(session_id)
        return False

    def purchase_product(self, session_id: str, shop_id: str, product_id: str) -> bool:
        if self.real:
            return self.real.purchase_product(session_id, shop_id, product_id)
        return False

    def open_shop(self, session_id: str, **shop_details) -> bool:
        if self.real:
            return self.real.open_shop(session_id, **shop_details)
        return False

    def get_personal_purchase_history(self, session_id: str) -> List[dict]:
        if self.real:
            return self.real.get_personal_purchase_history(session_id)
        return []

    def add_product_to_shop(self, session_id: str, shop_id: str, **product_info) -> bool:
        if self.real:
            return self.real.add_product_to_shop(session_id, shop_id, **product_info)
        return False

    def edit_product_info(self, session_id: str, shop_id: str, **product_info) -> bool:
        if self.real:
            return self.real.edit_product_info(session_id, shop_id, **product_info)
        return False

    def delete_product(self, session_id: str, shop_id: str, product_id: str) -> bool:
        if self.real:
            return self.real.delete_product(session_id, shop_id, product_id)
        return False

    def appoint_shop_owner(self, session_id: str, shop_id: str, username: str) -> bool:
        if self.real:
            return self.real.appoint_shop_owner(session_id, shop_id, username)
        return False

    def appoint_shop_manager(self, session_id: str, shop_id: str, username: str, permissions: dict) -> bool:
        if self.real:
            return self.real.appoint_shop_manager(session_id, shop_id, username, permissions)
        return False

    def edit_manager_permissions(self, session_id: str, shop_id: str, username: str, permissions: dict) -> bool:
        if self.real:
            return self.real.edit_manager_permissions(session_id, shop_id, username, permissions)
        return False

    def unappoint_shop_worker(self, session_id: str, shop_id: str, username: str) -> bool:
        if self.real:
            return self.real.unappoint_shop_worker(session_id, shop_id, username)
        return False

    def get_shop_staff_info(self, session_id: str, shop_id: str) -> List[dict]:
        if self.real:
            return self.real.get_shop_staff_info(session_id, shop_id)
        return []

    def get_shop_transaction_history(self, session_id: str, shop_id: str) -> List[dict]:
        if self.real:
            return self.real.get_shop_transaction_history(session_id, shop_id)
        return []

    def get_system_transaction_history(self, session_id: str) -> List[dict]:
        if self.real:
            return self.real.get_system_transaction_history(session_id)
        return []