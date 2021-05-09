from __future__ import annotations
import threading
from typing import List, Dict

from domain.commerce_system.appointment import Appointment, ShopOwner
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import Condition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.transaction_repo import TransactionRepo
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.shopping_cart import ShoppingCart


class User:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):
        self.user_state: UserState = Guest()
        self.counter_lock.acquire()
        self.id = self.__id_counter
        User.__id_counter = User.__id_counter + 1
        self.counter_lock.release()
        self.cart = ShoppingCart(self.id)

    def get_name(self):
        raise NotImplementedError()

    def login(self, sub_user: Subscribed):
        self.user_state = sub_user

    def register(self, username: str, **user_details):
        return self.user_state.register(username)

    def logout(self):
        self.user_state.logout()

    def purchase_product(self, shop: Shop, product: Product, amount_to_buy: int, payment_details: dict):
        bag = ShoppingBag(shop)
        bag.add_product(product, amount_to_buy)
        transaction = bag.purchase_bag(self.get_name(), payment_details)
        self._add_transaction(transaction)

    def purchase_shopping_bag(self, shop: Shop, payment_details: dict):
        bag = self.cart[shop]
        transaction = bag.purchase_bag(self.get_name(), payment_details)
        self._add_transaction(transaction)

    def purchase_cart(self, payment_details: dict, do_what_you_can=False):
        transactions = self.cart.purchase_cart(self.get_name(), payment_details, do_what_you_can)
        for transaction in transactions:
            self._add_transaction(transaction)

    def _add_transaction(self, transaction: Transaction):
        TransactionRepo.get_transaction_repo().add_transaction(transaction)
        self.user_state.add_transaction(transaction)

    def _remove_transaction(self, transaction: Transaction):
        self.user_state.remove_transaction(transaction)

    def save_product_to_cart(self, shop: Shop, product: Product, amount_to_buy: int) -> bool:
        return self.cart.add_product(product, shop, amount_to_buy)

    def remove_product_from_cart(self, shop: Shop, product: Product, amount: int) -> bool:
        return self.cart.remove_from_shopping_bag(shop, product, amount)

    def get_cart_info(self) -> dict:
        return self.cart.to_dict()

    def open_shop(self, **shop_details) -> Shop:
        raise NotImplementedError()

    def get_personal_transactions_history(self) -> List[Transaction]:
        return self.user_state.get_personal_transaction_history()

    def add_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def edit_product(self, shop: Shop, **product_details) -> Product:
        raise NotImplementedError()

    def delete_product(self, shop: Shop, product_id: str) -> Product:
        raise NotImplementedError()

    def appoint_shop_owner(self, shop: Shop, user) -> Appointment:
        raise NotImplementedError()

    def appoint_shop_manager(self, shop: Shop, user, permissions: List[str]) -> bool:
        raise NotImplementedError()

    def unappoint_shop_worker(self, shop: Shop, user) -> bool:
        raise NotImplementedError()

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        raise NotImplementedError()

    def get_shop_transaction_history(self, shop: Shop) -> List[Transaction]:
        raise NotImplementedError()

    def add_purchase_condition(self, shop: Shop, condition: Condition):
        raise NotImplementedError()

    def remove_purchase_condition(self, shop: Shop, condition_id: int):
        raise NotImplementedError()


class UserState:
    def get_name(self):
        return "Guest"

    def register(self, username: str, **user_details):
        raise Exception("Logged-in User cannot register")

    def appoint_manager(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        raise Exception("Guest User cannot appoint manager")

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop):
        raise Exception("Guest User cannot appoint owner")

    def get_appointment(self, shop: Shop):
        raise Exception("Guest User cannot get appointment")

    def add_product(self, shop: Shop, **product_info) -> Product:
        raise Exception("Guest User cannot add product")

    def edit_product(self, shop: Shop, product_id: int, **to_edit):
        raise Exception("Guest User cannot edit product")

    def delete_product(self, shop: Shop, product_id: int) -> bool:
        raise Exception("Guest User cannot delete product")

    def un_appoint_manager(self, owner_sub, shop: Shop):
        raise Exception("Guest User cannot un appoint manager")

    def un_appoint_owner(self, owner_sub, shop: Shop):
        raise Exception("Guest User cannot un appoint owner")

    def edit_manager_permissions(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]):
        raise Exception("Guest User cannot edit manager permissions")

    def get_personal_transaction_history(self):
        raise Exception("User cannot perform this action")

    def get_shop_transaction_history(self, shop: Shop):
        raise Exception("User cannot perform this action")

    def open_shop(self, shop_details):
        raise Exception("Guest User cannot edit manager permissions")

    def add_transaction(self, transaction: Transaction):
        pass

    def logout(self):
        raise Exception("User cannot logout in current state")

    def remove_transaction(self, transaction: Transaction):
        pass

    def get_system_transaction_history(self):
        raise Exception("only system administrator can see the system transaction history")

    def add_discount(self, shop, has_cond, condition, discount):
        raise Exception("User doesnt have permissions to manage discounts")

    def delete_discounts(self, shop, discount_ids):
        raise Exception("User doesnt have permissions to manage discounts")

    def aggregate_discounts(self, shop, discount_ids, func):
        raise Exception("User doesnt have permissions to manage discounts")

    def add_purchase_condition(self, shop: Shop, condition: Condition):
        raise Exception("User cannot perform this action")

    def remove_purchase_condition(self, shop: Shop, condition_id: int):
        raise Exception("User cannot perform this action")

    def get_permissions(self, shop):
        return {'delete': False, 'edit': False, 'add': False, 'discount': False, 'transaction': False, 'owner': False}


class Guest(UserState):
    def register(self, username: str, **user_details):
        return Subscribed(username)


class Subscribed(UserState):

    def __init__(self, username: str):
        self.appointments: Dict[Shop, Appointment] = {}
        self.username = username
        self.transactions: List[Transaction] = []

    def logout(self):
        pass

    """ calls personal appointment for the request. if doesnt have permission raises an exception"""
    def get_name(self):
        return self.username

    def appoint_manager(self, sub: Subscribed, shop: Shop, permissions: List[str]):
        session_app = self.get_appointment(shop)
        session_app.appoint_manager(sub, permissions)

    def appoint_owner(self, new_owner_sub: Subscribed, shop: Shop):
        owner_app = self.get_appointment(shop)
        owner_app.appoint_owner(new_owner_sub)

    def promote_manager_to_owner(self, manager_sub: Subscribed, shop: Shop):
        session_app: Appointment = self.get_appointment(shop)
        session_app.promote_manager_to_owner(manager_sub)

    def get_appointment(self, shop: Shop):
        if shop in self.appointments:
            return self.appointments[shop]
        raise Exception("no appointment for shop. shop id - ", shop.shop_id)

    def add_product(self, shop: Shop, **product_info) -> Product:
        return self.get_appointment(shop).add_product(**product_info)

    def edit_product(self, shop: Shop, product_id: int, **to_edit):
        self.get_appointment(shop).edit_product(product_id, **to_edit)

    def delete_product(self, shop: Shop, product_id: int):
        self.get_appointment(shop).delete_product(product_id)

    def un_appoint_manager(self, unappointed_manager, shop: Shop):
        unappointing_owner_app = self.get_appointment(shop)
        unappointing_owner_app.un_appoint_manager(unappointed_manager)

    def un_appoint_owner(self, owner_sub, shop: Shop):
        session_app = self.get_appointment(shop)
        session_app.un_appoint_owner(owner_sub)

    def edit_manager_permissions(self, manager_sub: Subscribed, shop: Shop, permissions: List[str]):
        owner_app = self.get_appointment(shop)
        owner_app.edit_manager_permissions(manager_sub, permissions)

    def open_shop(self, shop_details):
        new_shop = Shop(**shop_details)
        owner = ShopOwner(new_shop)
        new_shop.founder = owner
        self.appointments[new_shop] = owner
        return new_shop

    def get_shop_transaction_history(self, shop: Shop):
        app = self.get_appointment(shop)
        return app.get_shop_transaction_history()

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_personal_transaction_history(self):
        return self.transactions

    def add_discount(self, shop, has_cond, condition, discount):
        appointment = self.get_appointment(shop)
        appointment.add_discount(has_cond, condition, discount)

    def delete_discounts(self, shop, discount_ids):
        appointment = self.get_appointment(shop)
        appointment.delete_discount(discount_ids)

    def aggregate_discounts(self, shop, discount_ids, func):
        appointment = self.get_appointment(shop)
        appointment.aggregate_discounts(discount_ids, func)

    def add_purchase_condition(self, shop: Shop, condition: Condition):
        appointment = self.get_appointment(shop)
        appointment.add_purchase_condition(condition)

    def remove_purchase_condition(self, shop: Shop, condition_id: int):
        appointment = self.get_appointment(shop)
        appointment.remove_purchase_condition(condition_id)

    def get_permissions(self, shop):
        try:
            appointment = self.get_appointment(shop)
            appointment.get_permissions()
        except:
            print("!!!!!!!!!!!!!!!!!!!")
            return {'delete': False, 'edit': False, 'add': False, 'discount': False, 'transaction': False,
                    'owner': False}


class SystemManager(Subscribed):
    def __init__(self, username: str, system_transactions: TransactionRepo):
        super().__init__(username)
        self.system_transactions = system_transactions

    def get_system_transaction_history(self):
        return self.system_transactions.get_transactions()

    def get_system_transaction_history_of_shop(self,shop_id):
        return self.system_transactions.get_transactions_of_shop(shop_id)

    def get_system_transaction_history_of_user(self, username):
        return self.system_transactions.get_transactions_of_user(username)