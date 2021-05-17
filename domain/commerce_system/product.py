import threading
from typing import List

from data_model import ProductModel as Pm


class Product:
    __product_id = 1
    __id_lock = threading.Lock()

    def __init__(
            self, product_name: str, price: float, description: str = "",
            quantity: int = 0, categories: List[str] = None, shop_id=None
    ):
        if categories is None:
            categories = []
        Product.__id_lock.acquire()
        self.product_id = Product.__product_id
        Product.__product_id += 1
        Product.__id_lock.release()
        self.product_name = product_name
        self.price = price
        self.description = description
        self._quantity = 0
        self.set_quantity(quantity)
        self.categories: List[str] = categories
        self.shop_id = shop_id

    def to_dict(self):
        return {
            Pm.PRODUCT_ID: self.product_id,
            Pm.PRODUCT_NAME: self.product_name,
            Pm.PRODUCT_DESC: self.description,
            Pm.PRICE: self.price,
            Pm.QUANTITY: self._quantity,
            Pm.CATEGORIES: self.categories,
            Pm.SHOP_ID: self.shop_id
        }

    def set_quantity(self, new_quantity):
        assert new_quantity >= 0, "product quantity must be non-negative"
        self._quantity = new_quantity
        return True

    def get_quantity(self):
        return self._quantity
