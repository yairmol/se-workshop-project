import threading
from typing import Dict, List

from domain.commerce_system.product import Product
from domain.commerce_system.transaction import Transaction
from data_model import ShopModel as Sm


class Shop:
    __shop_id = 0

    def __init__(self, shop_id: int, shop_name, description=""):
        self.shop_id = Shop.__shop_id
        Shop.__shop_id += 1
        self.shop_id = shop_id
        self.name: str = shop_name
        self.description: str = description
        self.products: Dict[int, Product] = {}
        self.transaction_history: List[Transaction] = []
        self.products_lock = threading.Lock()
        self.managers_lock = threading.Lock()
        self.owners_lock = threading.Lock()
        self.shop_managers = {}
        self.shop_owners = {}

    def to_dict(self):
        ret = {
            Sm.SHOP_ID: self.shop_id,
            Sm.SHOP_NAME: self.name,
            Sm.SHOP_PRODS: list(map(lambda p: p.to_dict(), self.products.values())),
            Sm.SHOP_DESC: self.description,
        }
        return ret

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
    def edit_product(self, product_id, **to_edit):
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

    def add_transaction(self, bag: dict, transaction: Transaction) -> bool:
        self.products_lock.acquire()
        for product, amount in bag:
            if product.quantity < amount:
                return False
        for product, amount in bag:
            product.quantity -= amount
        self.transaction_history.append(
            Transaction(self, transaction.products, transaction.payment_details, transaction.date, transaction.price)
        )
        self.products_lock.release()
        return True

    def remove_transaction(self, bag: dict, transaction: Transaction):
        self.products_lock.acquire()
        for product, amount in bag:
            product.quantity += amount
        self.transaction_history.remove(transaction)
        self.products_lock.release()

    def add_manager(self, manager_sub):
        self.managers_lock.acquire()
        self.shop_managers[manager_sub.username] = manager_sub
        self.managers_lock.release()

    def add_owner(self, owner_sub):
        self.owners_lock.acquire()
        self.shop_managers[owner_sub.username] = owner_sub
        self.owners_lock.release()

    def display_managers_info(self):

    def display_owners_info(self):