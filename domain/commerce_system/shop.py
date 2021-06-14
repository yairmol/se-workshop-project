import threading
from typing import Dict, List, TypeVar

from sqlalchemy import orm

from data_access_layer.engine import add_to_session
from domain.commerce_system.action import Action, ActionPool
from domain.commerce_system.purchase_conditions import Condition, CompositePurchaseCondition
from domain.discount_module.discount_calculator import AdditiveDiscount, Discount
from domain.commerce_system.product import Product, PurchaseType
from domain.commerce_system.transaction import Transaction
from data_model import ShopModel as Sm
from domain.discount_module.discount_management import DiscountManagement, DiscountDict, ConditionRaw

SHOP_ID = "shopId"
SHOP_NAME = "shopName"
SHOP_DESC = "shopDesc"
SHOP_IMAGE = "shopImage"

WORKER_NAME = "username"
WORKER_TITLE = "title"
WORKER_APPOINTER = "appointer"
PERMISSIONS = "permissions"

T_app = TypeVar('T_app')


class Shop:
    __shop_id = 1

    def __init__(self, shop_name: str, description="", image_url=""):
        self.founder = None
        self.shop_id = Shop.__shop_id
        Shop.__shop_id += 1
        self.name: str = shop_name
        self.description: str = description
        self.products: Dict[int, Product] = {}
        self.transaction_history: List[Transaction] = []
        self.products_lock = threading.Lock()
        self.workers_lock = threading.Lock()
        self.discount_lock = threading.Lock()
        self.workers = {}
        self.discount = AdditiveDiscount([])
        self.image_url = image_url
        self.conditions: List[Condition] = []

    @add_to_session
    def get_founder(self):
        return self.founder

    @add_to_session
    def get_shop_id(self):
        return self.shop_id

    @add_to_session
    def get_name(self):
        return self.name

    @add_to_session
    def get_description(self):
        return self.description

    @add_to_session
    def get_products(self):
        return self.products

    @add_to_session
    def get_transaction_history(self):
        return self.transaction_history

    @add_to_session
    def get_workers(self):
        return self.workers

    @add_to_session
    def get_discount(self):
        return self.discount

    @add_to_session
    def get_image_url(self):
        return self.image_url

    @add_to_session
    def get_conditions(self):
        return self.conditions

    @orm.reconstrutor
    def load_from_int(self):
        self.products_lock = threading.Lock()
        self.workers_lock = threading.Lock()
        self.discount_lock = threading.Lock()

    def to_dict(self, include_products=True):
        ret = {
            Sm.SHOP_ID: self.get_shop_id(),
            Sm.SHOP_NAME: self.get_name(),
            Sm.SHOP_DESC: self.get_description(),
            Sm.SHOP_IMAGE: self.get_image_url(),
        }
        if include_products:
            ret[Sm.SHOP_PRODS] = list(map(lambda p: p.to_dict(), self.get_products().values()))
        return ret

    def add_product(self, **product_info) -> Product:
        """ returns product_id if successful"""
        with self.products_lock:
            assert not self.has_product(product_info["product_name"]), \
                f"product name {product_info['product_name']} is not unique"
            product = Product(**product_info, shop_id=self.get_shop_id())
            self.get_products()[product.product_id] = product
            return product

    def delete_product(self, product_id: int) -> bool:
        with self.products_lock:
            assert product_id in self.get_products().keys(), f"shop1 does not hold product with id - {product_id}"
            self.get_products().pop(product_id)
            return True

    def edit_product(self, product_id, **to_edit) -> bool:
        """
        edit product receives product id and a dict of fields to alter and the new values.
        MAKE SURE THE FIELD NAMES ARE ACCURATE
        """
        with self.products_lock:
            assert product_id in self.get_products(), f"no product with id={product_id}"
            product = self.get_products()[product_id]
            for field, new_value in to_edit.items():
                if field == "quantity":
                    product.set_quantity(new_value)
                    continue
                if field == "purchase_types":
                    product.set_purchase_types(new_value)
                    continue
                if field == "categories":
                    product.set_categories(new_value)
                    continue
                if not hasattr(product, field):
                    raise Exception("product has no field ", field)
                setattr(product, field, new_value)
        return True

    @add_to_session
    def has_product(self, product_name: str):
        """ return true if shop has product named product_name"""
        found = False
        for supply_product in self.get_products().values():
            found = found or supply_product.product_name == product_name
        return found

    def get_id(self, product_name: str):
        """ returns id of first product named product_name"""
        product_id = -1
        for p_id, supply_product in self.get_products().items():
            if supply_product.product_name == product_name:
                product_id = p_id
        return product_id

    def add_transaction(self, bag, transaction: Transaction) -> bool:
        with self.products_lock:
            product_update_actions = ActionPool([
                Action(product.set_quantity, product.get_quantity() - bag_info.amount)
                .set_reverse(Action(product.set_quantity, product.get_quantity()))
                for product, bag_info in bag
            ])
            product_update_actions.execute_actions()
            self.get_transaction_history().append(transaction)
            return True

    def cancel_transaction(self, bag: dict, transaction: Transaction) -> bool:
        with self.products_lock:
            for product, bag_info in bag:
                product.set_quantity(product.get_quantity() + bag_info.amount)
            self.get_transaction_history().remove(transaction)
            return True

    def add_manager(self, manager_app) -> bool:
        with self.workers_lock:
            self.get_workers()[manager_app.username] = manager_app
            return True

    def add_owner(self, owner_app) -> bool:
        with self.workers_lock:
            self.get_workers()[owner_app.username] = owner_app
            return True

    def remove_manager(self, manager_sub) -> bool:
        with self.workers_lock:
            self.get_workers().pop(manager_sub.username)
            return True

    def remove_owner(self, owner_sub) -> bool:
        with self.workers_lock:
            self.get_workers().pop(owner_sub.username)
            return True

    def get_staff_info(self) -> List[T_app]:
        with self.workers_lock:
            return list(self.get_workers().values())

    def get_shop_transaction_history(self) -> List[Transaction]:
        return list(self.get_transaction_history())

    def get_product_info(self, product_id) -> Product:
        assert product_id in self.get_products(), "product id doesn't exists"
        return self.get_products().get(product_id)

    def get_discounts(self) -> List[Discount]:
        return self.get_discount().discounts

    def add_discount(self, has_cond: bool, condition: ConditionRaw, discount: DiscountDict) -> Discount:
        with self.discount_lock:
            return DiscountManagement.add_discount(self.get_discount(), has_cond, condition, discount)

    def aggregate_discounts(self, discount_ids: [int], func: str) -> bool:
        with self.discount_lock:
            self.get_discount().aggregate_discounts(discount_ids, func)
        return True

    def move_discount_to(self, src_discount_id: int, dst_discount_id: int) -> bool:
        with self.discount_lock:
            discount = DiscountManagement.remove(self.get_discount(), src_discount_id)
            DiscountManagement.add(self.get_discount(), dst_discount_id, discount)
        return True

    def delete_discounts(self, discount_ids) -> bool:
        with self.discount_lock:
            for d_id in discount_ids:
                DiscountManagement.remove(self.get_discount(), d_id)
        return True

    def get_purchase_conditions(self) -> List[Condition]:
        return self.get_conditions()

    def add_purchase_condition(self, condition: Condition) -> bool:
        self.get_conditions().append(condition)
        return True

    def remove_purchase_condition(self, condition_id: int) -> bool:
        def remove(conds: List[Condition], cond_id: int):
            for c in conds:
                if c.id == cond_id:
                    conds.remove(c)
                    return True
                if isinstance(c, CompositePurchaseCondition):
                    res = remove(c.conditions, cond_id)
                    if res:
                        return True
            return False
        success = remove(self.get_conditions(), condition_id)
        return success

    def add_purchase_type(self, product_id: int, purchase_type_info: dict) -> PurchaseType:
        return self.get_products()[product_id].add_purchase_type(purchase_type_info)

    def add_price_offer(self, username: str, product_id: int, offer: float) -> bool:
        return self.get_products()[product_id].add_price_offer(username, offer)

    def reply_price_offer(self, product_id: int, offer_maker: str, action: str) -> bool:
        return self.get_products()[product_id].reply_price_offer(offer_maker, action)
