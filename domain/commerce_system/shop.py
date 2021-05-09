import threading
from typing import Dict, List

from domain.commerce_system.action import Action, ActionPool
from domain.discount_module.discount_calculator import AdditiveDiscount
from domain.commerce_system.product import Product
from domain.commerce_system.transaction import Transaction
from data_model import ShopModel as Sm
from domain.discount_module.discount_management import SimpleCond, DiscountManagement, DiscountDict

SHOP_ID = "shopId"
SHOP_NAME = "shopName"
SHOP_DESC = "shopDesc"
SHOP_IMAGE = "shopImage"

WORKER_NAME = "name"
WORKER_TITLE = "title"
WORKER_APPOINTER = "appointer"
PERMISSIONS = "permissions"

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
        self.discount_lock = threading.Lock()
        self.shop_managers = {}
        self.shop_owners = {}
        self.discount = AdditiveDiscount([])
        self.imageUrl = ""

    def to_dict(self, include_products=True):
        ret = {
            Sm.SHOP_ID: self.shop_id,
            Sm.SHOP_NAME: self.name,
            Sm.SHOP_DESC: self.description,
            Sm.SHOP_IMAGE: self.imageUrl,
        }
        if include_products:
            ret[Sm.SHOP_PRODS] = list(map(lambda p: p.to_dict(), self.products.values()))
        return ret

    def add_product(self, **product_info) -> Product:
        """ returns product_id if successful"""
        with self.products_lock:
            assert not self.has_product(product_info["product_name"]), \
                f"product name {product_info['product_name']} is not unique"
            product = Product(**product_info)
            self.products[product.product_id] = product
            return product

    def delete_product(self, product_id: int):
        with self.products_lock:
            assert product_id in self.products.keys(), f"shop1 does not hold product with id - {product_id}"
            self.products.pop(product_id)

    def edit_product(self, product_id, **to_edit):
        """
        edit product receives product id and a dict of fields to alter and the new values.
        MAKE SURE THE FIELD NAMES ARE ACCURATE
        """
        with self.products_lock:
            assert product_id in self.products, f"no product with id={product_id}"
            product = self.products[product_id]
            for field, new_value in to_edit.items():
                if field == "quantity":
                    product.set_quantity(new_value)
                    continue
                if not hasattr(product, field):
                    raise Exception("product has no field ", field)
                setattr(product, field, new_value)

    def get_free_id(self) -> int:
        last_id = 1
        for product_id in sorted(self.products.keys()):
            if product_id > last_id + 1:
                return last_id + 1
            last_id = product_id
        return last_id + 1

    def has_product(self, product_name: str):
        """ return true if shop has product named product_name"""
        found = False
        for supply_product in self.products.values():
            found = found or supply_product.product_name == product_name
        return found

    def get_id(self, product_name: str):
        """ returns id of first product named product_name"""
        product_id = -1
        for p_id, supply_product in self.products.items():
            if supply_product.product_name == product_name:
                product_id = p_id
        return product_id

    def add_transaction(self, bag, transaction: Transaction) -> bool:
        with self.products_lock:
            product_update_actions = ActionPool([
                Action(product.set_quantity, product.get_quantity() - amount)
                    .set_reverse(Action(product.set_quantity, product.get_quantity()))
                for product, amount in bag
            ])
            product_update_actions.execute_actions()
            self.transaction_history.append(transaction)
            return True

    def cancel_transaction(self, bag: dict, transaction: Transaction):
        with self.products_lock:
            for product, amount in bag:
                product.set_quantity(product.get_quantity() + amount)
            self.transaction_history.remove(transaction)

    def add_manager(self, manager_sub):
        with self.managers_lock:
            self.shop_managers[manager_sub.username] = manager_sub

    def add_owner(self, owner_sub):
        with self.owners_lock:
            self.shop_owners[owner_sub.username] = owner_sub

    def remove_manager(self, manager_sub):
        with self.managers_lock:
            self.shop_managers.pop(manager_sub.username)

    def remove_owner(self, owner_sub):
        with self.owners_lock:
            self.shop_owners.pop(owner_sub.username)

    def get_manager_info(self, sub):
        return {
            WORKER_NAME: sub.username,
            WORKER_TITLE: "manager",
            WORKER_APPOINTER: sub.get_appointment(self).appointer.username,
            PERMISSIONS: sub.get_appointment(self).permissions
        }

    def get_owner_info(self, sub):
        return {
            WORKER_NAME: sub.username,
            WORKER_TITLE: "owner" if sub != self.founder else "founder",
            WORKER_APPOINTER: sub.get_appointment(self).appointer.username
        }

    def get_managers_info(self):
        info_dicts = []
        self.managers_lock.acquire()
        for manager_sub in self.shop_managers.values():
            info_dicts += [self.get_manager_info(manager_sub)]
        self.managers_lock.release()
        return info_dicts

    def get_owners_info(self):
        info_dicts = []
        with self.owners_lock:
            for owner_sub in self.shop_owners.values():
                info_dicts += [self.get_owner_info(owner_sub)]
            return info_dicts

    def get_staff_info(self):
        return self.get_managers_info() + self.get_owners_info()

    def get_shop_transaction_history(self):
        return list(map(lambda x: x.to_dict(), self.transaction_history))

    def get_product_info(self, product_id):
        assert product_id in self.products, "product id doesn't exists"
        return self.products.get(product_id)

    def add_discount(self, has_cond: bool, condition: [str or SimpleCond or []], discount: DiscountDict):
        self.discount_lock.acquire()
        DiscountManagement.add_discount(self.discount, has_cond, condition, discount)
        self.discount_lock.release()

    def aggregate_discounts(self, discount_ids: [int], func: str):
        self.discount_lock.acquire()
        self.discount.aggregate_discounts(discount_ids,func)
        self.discount_lock.release()

    def delete_discounts(self, discount_ids):
        self.discount_lock.acquire()
        self.discount.delete_discounts(discount_ids)
        self.discount_lock.release()