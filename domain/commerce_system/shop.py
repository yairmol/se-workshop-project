import threading
from typing import Dict, List

from domain.commerce_system.product import Product
from domain.commerce_system.transaction import Transaction
from data_model import ShopModel as Sm

WORKER_NAME = "name"
WORKER_TITLE = "title"
WORKER_APPOINTER = "appointer"


class Shop:
    __shop_id = 1

    def __init__(self, shop_name: str, description=""):
        self.founder = None
        self.shop_id = Shop.__shop_id
        Shop.__shop_id += 1
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
    def add_product(self, **product_info):
        self.products_lock.acquire()
        try:
            assert not self.has_product(product_info["product_name"]), f"product name {product_info['product_name']} is not unique"
            product = Product(**product_info)
            self.products[product.product_id] = product
        except Exception as e:
            self.products_lock.release()
            raise e
        self.products_lock.release()
        return product.product_id

    def delete_product(self, product_id: int):
        self.products_lock.acquire()
        try:
            assert product_id in self.products.keys(), f"shop does not hold product with id - {product_id}"
            self.products.pop(product_id)
        except Exception as e:
            self.products_lock.release()
            raise e
        self.products_lock.release()

    """ edit product receives product id and a dict of fields to alter and the new values.
        MAKE SURE THE FIELD NAMES ARE ACCURATE"""
    def edit_product(self, product_id, **to_edit):
        self.products_lock.acquire()
        try:
            assert product_id in self.products, f"no product with id={product_id}"
            product = self.products[product_id]
            for field, new_value in to_edit.items():
                if not hasattr(product, field):
                    raise Exception("product has no field ", field)
                setattr(product, field, new_value)
        except Exception as e:
            self.products_lock.release()
            raise e
        self.products_lock.release()

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
            found = found or supply_product.product_name == product_name
        return found

    """ returns id of first product named product_name"""
    def get_id(self, product_name: str):
        product_id = -1
        for p_id, supply_product in self.products.items():
            if supply_product.product_name == product_name:
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
        self.shop_owners[owner_sub.username] = owner_sub
        self.owners_lock.release()

    def remove_manager(self, manager_sub):
        self.managers_lock.acquire()
        self.shop_managers.pop(manager_sub.username)
        self.managers_lock.release()

    def remove_owner(self, owner_sub):
        self.owners_lock.acquire()
        self.shop_owners.pop(owner_sub.username)
        self.owners_lock.release()

    def get_manager_info(self, sub):
        return {WORKER_NAME: sub.username, WORKER_TITLE: "manager", WORKER_APPOINTER: sub.get_appointment(self).appointer.username}

    def get_owner_info(self, sub):
        return {WORKER_NAME: sub.username, WORKER_TITLE: "manager" if sub != self.founder else "founder", WORKER_APPOINTER: sub.get_appointment(self).appointer.username}

    def get_managers_info(self):
        info_dicts = []
        self.managers_lock.acquire()
        for manager_sub in self.shop_managers.values():
            info_dicts += [self.get_manager_info(manager_sub)]
        self.managers_lock.release()
        return info_dicts

    def get_owners_info(self):
        info_dicts = []
        self.owners_lock.acquire()
        for owner_sub in self.shop_owners.values():
            info_dicts += [self.get_owner_info(owner_sub)]
        self.owners_lock.release()
        return info_dicts

    def get_staff_info(self):
        return self.get_managers_info() + self.get_owners_info()

    def get_shop_transaction_history(self):
        return list(map(lambda x: x.to_dict(), self.transaction_history))
