import threading
from typing import Dict

from domain.commerce_system.product import Product
from domain.commerce_system.productDTO import ProductDTO
from domain.commerce_system.transactionDTO import TransactionDTO


SHOP_NAME = "shop_name"
SHOP_DESC = "description"
SHOP_ID = "shop_id"
SHOP_PRODS = "products"


class Shop:
    def __init__(self, shop_id: int, **shop_info):
        self.shop_id = shop_id
        assert SHOP_NAME in shop_info
        self.name: str = shop_info[SHOP_NAME]
        self.description: str = shop_info.get(SHOP_DESC, "")
        self.products: Dict[int, Product] = {}
        self.transaction_history = []
        self.products_lock = threading.Lock()

    def to_dict(self):
        ret = {
            SHOP_ID: self.shop_id,
            SHOP_NAME: self.name,
            SHOP_PRODS: list(map(lambda p: p.to_dict(), self.products.values()))
        }
        if self.description:
            ret[SHOP_DESC] = self.description
        return ret

    """ quantity has to be no more than available product quantity"""
    def sell_product(self, product_id: str, quantity: int, payment_details: dict) -> bool: # add payment
        available_quantity = self.products[product_id].quantity
        if available_quantity < quantity:
            return False
        return True

    """ returns product_id if successful"""
    def add_product(self, product: Product) -> int:
        product_id = self.get_free_id()
        self.products[product_id] = product
        return product_id

    def delete_product(self, product_id: int) -> bool:
        res = self.products.pop(product_id, 0)
        return res != 0

    """ edit product receives product id and a dict of fields to alter and the new values.
        MAKE SURE THE FIELD NAMES ARE ACCURATE"""
    def edit_product(self, product_id, **to_edit) -> bool:
        if product_id not in self.products:
            raise Exception("no product with id=", product_id)
        product = self.products[product_id]
        for field, new_value in to_edit.items():
            if field not in product.__dict__:
                raise Exception("product has no field ", field)
            product.__dict__[field] = new_value

    def get_shop_info(self) -> str:
        s = ""
        for p_id, p_val in self.products:
            s += "store product id: ", p_id, "\nproduct id: ", p_val.product_id, "\nproduct name: ",\
                 p_val.name, "\nprice: ", p_val.price
        return s

    def get_free_id(self) -> int:
        last_id = 1
        for product_id in sorted(self.products.keys()):
            if product_id > last_id + 1:
                return last_id + 1
            last_id = product_id
        return last_id + 1

    """ return true if shop has product named product_name"""
    def has_product(self, product_name: str):
        found = False
        for supply_product in self.products.values():
            found = found or supply_product.name == product_name
        return found

    """ returns id of first product named product_name"""
    def get_id(self, product_name: str):
        product_id = -1
        for p_id, supply_product in self.products.items():
            if supply_product.name == product_name:
                product_id = p_id
        return product_id

    def add_transaction(self, bag: dict, transaction: TransactionDTO) -> bool:
        self.products_lock.aquire()
        for product, amount in bag:
            if product.quantity < amount:
                return False
        for product, amount in bag:
            product.quantity -= amount
        self.transaction_history += [TransactionDTO(self, transaction.products, transaction.payment_details, transaction.date, transaction.price)]
        self.products_lock.release()
        return True

    def remove_transaction(self, bag: dict, transaction: TransactionDTO):
        self.products_lock.aquire()
        for product, amount in bag:
            product.quantity += amount
        self.transaction_history.remove(transaction)
        self.products_lock.release()
