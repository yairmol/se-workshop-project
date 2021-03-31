from typing import List
from commerce_system.utils import Transaction
from shop import IShop
from product import Product


class IUser:
    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError()

    def register(self, username: str, email: str, password: str, **user_details) -> bool:
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def buy_product(self, shop: IShop, product_id: str, payment_details: dict) -> bool:
        raise NotImplementedError()

    def buy_shopping_bag(self, shop: IShop, payment_details: dict):
        raise NotImplementedError()

    def buy_cart(self, payment_details: dict) -> bool:
        raise NotImplementedError()

    def save_product_to_cart(self, shop: IShop, product_id: str) -> bool:
        raise NotImplementedError()

    def get_cart_info(self) -> List[dict]:
        raise NotImplementedError()

    def open_shop(self, **shop_details) -> IShop:
        raise NotImplementedError()

    def get_personal_transactions_history(self) -> List[Transaction]:
        raise NotImplementedError()

    def add_product(self, shop: IShop, **product_details) -> Product:
        raise NotImplementedError()

    def edit_product(self, shop: IShop, **product_details) -> Product:
        raise NotImplementedError()

    def delete_product(self, shop: IShop, product_id: str) -> Product:
        raise NotImplementedError()
