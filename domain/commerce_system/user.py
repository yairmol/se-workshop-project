from __future__ import annotations
import threading
from typing import List, Dict, Iterable
from sqlalchemy import orm

from data_access_layer.engine import add_to_session, save
from data_access_layer.subscribed_repository import save_subscribed
from domain.commerce_system.appointment import Appointment, ShopOwner
from domain.commerce_system.product import Product, PurchaseType, PurchaseOffer
from domain.commerce_system.purchase_conditions import Condition
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingBag
from domain.commerce_system.transaction_repo import TransactionRepo
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.shopping_cart import ShoppingCart
from domain.discount_module.discount_calculator import Discount
from data_model import UserModel as UserM
from domain.discount_module.discount_management import DiscountDict, ConditionRaw
from domain.notifications.notifications import Notifications


class User:
    __id_counter = 1
    counter_lock = threading.Lock()

    def __init__(self):
        self.user_state: UserState = Guest()
        self.counter_lock.acquire()
        self.id = self.__id_counter
        User.__id_counter = User.__id_counter + 1
        self.counter_lock.release()
        self.cart = ShoppingCart()
        self.notifications = Notifications.get_notifications()
        self.notifications.add_client(self.id)

    def send_message(self, msg):
        self.notifications.send_message(self.id, msg)

    def send_error(self, msg):
        self.notifications.send_error(self.id, msg)

    def get_name(self) -> str:
        return self.user_state.get_name(self.id)

    def login(self, sub_user: Subscribed) -> bool:
        self.user_state.login()
        self.user_state = sub_user
        sub_user.on_login(self.id)
        return True

    def register(self, username: str, **user_details) -> Subscribed:
        return self.user_state.register(username, **user_details)

    def logout(self) -> bool:
        self.user_state.logout()
        self.user_state = Guest()
        return True

    def purchase_product(self, shop: Shop, product: Product, amount_to_buy: int, payment_details: dict,
                         delivery_details: dict) -> Transaction:
        bag = ShoppingBag(shop)
        bag.add_product(product, amount_to_buy)
        transaction = bag.purchase_bag(self.get_name(), payment_details, delivery_details)
        self._add_transaction(transaction)
        return transaction

    def purchase_shopping_bag(self, shop: Shop, payment_details: dict, delivery_details: dict) -> Transaction:
        bag = self.cart[shop]
        transaction = bag.purchase_bag(self.get_name(), payment_details, delivery_details)
        self._add_transaction(transaction)
        return transaction

    def purchase_cart(self, payment_details: dict, delivery_details: dict, do_what_you_can=False) -> List[Transaction]:
        transactions = self.cart.purchase_cart(self.get_name(), payment_details, delivery_details, do_what_you_can)
        for transaction in transactions:
            self._add_transaction(transaction)
        return transactions

    def _add_transaction(self, transaction: Transaction) -> None:
        TransactionRepo.get_transaction_repo().add_transaction(transaction)
        self.user_state.add_transaction(transaction)

    def _remove_transaction(self, transaction: Transaction) -> None:
        self.user_state.remove_transaction(transaction)

    def save_product_to_cart(self, shop: Shop, product: Product, amount_to_buy: int,
                             purchase_type_id=None, **pt_args) -> bool:
        return self.cart.add_product(product, shop, amount_to_buy, purchase_type_id, **pt_args)

    def remove_product_from_cart(self, shop: Shop, product: Product, amount: int) -> bool:
        return self.cart.remove_from_shopping_bag(shop, product, amount)

    def get_cart_info(self) -> dict:
        return self.cart.to_dict()

    def open_shop(self, **shop_details) -> Shop:
        return self.user_state.open_shop(**shop_details)

    def get_personal_transactions_history(self) -> List[Transaction]:
        return self.user_state.get_personal_transaction_history()

    def add_product(self, shop: Shop, **product_details) -> Product:
        return self.user_state.add_product(shop, **product_details)

    def edit_product(self, shop: Shop, **product_details) -> bool:
        return self.user_state.edit_product(shop, **product_details)

    def delete_product(self, shop: Shop, product_id: int) -> bool:
        return self.user_state.delete_product(shop, product_id)

    def appoint_shop_owner(self, shop: Shop, user: Subscribed) -> Appointment:
        return self.user_state.appoint_owner(user, shop)

    def appoint_shop_manager(self, shop: Shop, user: Subscribed, permissions: List[str]) -> Appointment:
        return self.user_state.appoint_manager(user, shop, permissions)

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        return self.user_state.get_shop_staff_info(shop)

    def get_shop_transaction_history(self, shop: Shop) -> List[Transaction]:
        return self.user_state.get_shop_transaction_history(shop)

    def add_purchase_condition(self, shop: Shop, condition: Condition) -> bool:
        return self.user_state.add_purchase_condition(shop, condition)

    def remove_purchase_condition(self, shop: Shop, condition_id: int) -> bool:
        return self.user_state.remove_purchase_condition(shop, condition_id)

    def get_shop_discounts(self, shop: Shop) -> Iterable[Discount]:
        return self.user_state.get_shop_discounts(shop)

    def get_shop_purchase_conditions(self, shop: Shop) -> List[Condition]:
        return self.user_state.get_shop_purchase_conditions(shop)

    def to_dict(self) -> dict:
        ret = {
            "id": self.id
        }
        ret.update(self.user_state.to_dict())
        return ret

    def exit(self):
        self.notifications.disconnect(self.id)

    def add_purchase_type(self, shop: Shop, product_id: int, purchase_type_info: dict) -> PurchaseType:
        return self.user_state.add_purchase_type(shop, product_id, purchase_type_info)

    def offer_price(self, shop: Shop, product_id: int, offer: float) -> bool:
        return self.user_state.offer_price(shop, product_id, offer)

    def reply_price_offer(self, shop: Shop, product_id: int, offer_maker: str, action: str) -> bool:
        return self.user_state.reply_price_offer(shop, product_id, offer_maker, action)

    def change_product_purchase_type(self, shop: Shop, product_id: int, purchase_type_id: int, pt_args: dict) -> bool:
        return self.cart.change_product_purchase_type(shop, product_id, purchase_type_id, pt_args)

    def get_shop_info(self, shop: Shop):
        self.user_state.get_shop_info(shop)

    def get_offers(self, shop: Shop, product_id: int) -> List[PurchaseOffer]:
        return self.user_state.get_offers(shop, product_id)


class UserState:
    def get_name(self, userid=None) -> str:
        raise NotImplementedError()

    def send_error(self, msg):
        raise NotImplementedError()

    def send_message(self, msg):
        raise NotImplementedError()

    def register(self, username: str, **user_detail) -> Subscribed:
        raise Exception("Logged-in User cannot register")

    def login(self) -> bool:
        raise NotImplementedError()

    def appoint_manager(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]) -> Appointment:
        raise Exception("Guest User cannot appoint manager")

    def appoint_owner(self, owner_sub: Subscribed, shop: Shop) -> Appointment:
        raise Exception("Guest User cannot appoint owner")

    def promote_manager_to_owner(self, manager_sub: Subscribed, shop: Shop) -> Appointment:
        raise Exception("Guest User cannot appoint owner")

    def get_appointment(self, shop: Shop) -> Appointment:
        raise Exception("Guest User cannot get appointment")

    def add_product(self, shop: Shop, **product_info) -> Product:
        raise Exception("Guest User cannot add product")

    def edit_product(self, shop: Shop, product_id: int, **to_edit) -> bool:
        raise Exception("Guest User cannot edit product")

    def delete_product(self, shop: Shop, product_id: int) -> bool:
        raise Exception("Guest User cannot delete product")

    def un_appoint_manager(self, owner_sub, shop: Shop) -> bool:
        raise Exception("Guest User cannot un appoint manager")

    def un_appoint_owner(self, owner_sub, shop: Shop) -> bool:
        raise Exception("Guest User cannot un appoint owner")

    def edit_manager_permissions(self, owner_sub: Subscribed, shop: Shop, permissions: List[str]) -> bool:
        raise Exception("Guest User cannot edit manager permissions")

    def get_personal_transaction_history(self) -> List[Transaction]:
        raise Exception("User cannot perform this action")

    def get_shop_transaction_history(self, shop: Shop) -> List[Transaction]:
        raise Exception("User cannot perform this action")

    def open_shop(self, shop_details) -> Shop:
        raise Exception("Guest User cannot edit manager permissions")

    def add_transaction(self, transaction: Transaction) -> bool:
        pass

    def logout(self) -> bool:
        raise Exception("User cannot logout in current state")

    def remove_transaction(self, transaction: Transaction) -> bool:
        pass

    def get_system_transaction_history(self) -> List[Transaction]:
        raise Exception("only system administrator can see the system transaction history")

    def get_shop_discounts(self, shop: Shop) -> Iterable[Discount]:
        raise Exception("User doesn't have permissions to get shop discounts")

    def add_discount(self, shop: Shop, has_cond: bool, condition: ConditionRaw, discount: DiscountDict) -> Discount:
        raise Exception("User doesnt have permissions to manage discounts")

    def delete_discounts(self, shop: Shop, discount_ids: List[int]) -> bool:
        raise Exception("User doesnt have permissions to manage discounts")

    def aggregate_discounts(self, shop: Shop, discount_ids: List[int], func: str) -> bool:
        raise Exception("User doesnt have permissions to manage discounts")

    def move_discount_to(self, shop: Shop, src_discount_id: int, dst_discount_id: int) -> bool:
        raise Exception("User doesnt have permissions to manage discounts")

    def get_shop_purchase_conditions(self, shop: Shop) -> List[Condition]:
        raise Exception("User doesn't have permissions to get shop purchase conditions")

    def add_purchase_condition(self, shop: Shop, condition: Condition) -> bool:
        raise Exception("User cannot perform this action")

    def remove_purchase_condition(self, shop: Shop, condition_id: int) -> bool:
        raise Exception("User cannot perform this action")

    def get_permissions(self, shop) -> Dict[str, bool]:
        return {'delete': False, 'edit': False, 'add': False, 'discount': False, 'transaction': False, 'owner': False}

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        raise Exception("User doesn't have permission to see shop staff")

    def get_appointments(self) -> List[Appointment]:
        raise Exception("User doesn't have permission to get appointments")

    def get_system_transaction_history_of_shop(self, shop_id: int):
        raise Exception("User doesn't have system manager permissions")

    def get_system_transaction_history_of_user(self, username: str):
        raise Exception("User doesn't have system manager permissions")

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def add_purchase_type(self, shop: Shop, product_id: int, purchase_type_info: dict) -> PurchaseType:
        raise Exception("User doesn't have permission to edit purchase types")

    def offer_price(self, shop: Shop, product_id: int, offer: float) -> bool:
        raise Exception("user must be signed in to make a purchase offer")

    def reply_price_offer(self, shop: Shop, product_id: int, offer_maker: str, action: str) -> bool:
        raise Exception("User doesn't have permission to reply to a price offer")

    def get_shop_info(self, shop: Shop):
        return shop.to_dict()

    def get_offers(self, shop: Shop, product_id: int) -> List[PurchaseOffer]:
        raise Exception("user doesn't have permission to get offers")


class Guest(UserState):
    def get_name(self, userid=None):
        return f"Guest-{hash(userid) if userid else 'None'}"

    def register(self, username: str, **user_details):
        sub = Subscribed(username)
        save(sub)
        return sub

    def to_dict(self):
        return {UserM.USERNAME: self.get_name()}

    def login(self):
        return True


class Subscribed(UserState):

    def __init__(self, username: str):
        self.appointments: Dict[Shop, Appointment] = {}
        self.username = username
        self.transactions: List[Transaction] = []
        self.pending_messages = []
        self.logged_user = None
        self.notifications = Notifications.get_notifications()

    @orm.reconstructor
    def init_on_load(self):
        self.notifications = Notifications.get_notifications()
        self.pending_messages = []
        self.appointments: Dict[Shop, Appointment] = {} # TODO Remove this when commiting

    def get_self(self): return self

    @add_to_session
    def on_login(self, logged_user):
        self.logged_user = logged_user
        # print("on login")
        self.notifications.on_sub_login(logged_user, self.username)
        for msg in self.pending_messages:
            self.send_message(msg)

    @add_to_session
    def send_message(self, msg):
        if self.logged_user:
            self.notifications.send_message(self.logged_user, msg)
        else:
            self.pending_messages.append(msg)

    @add_to_session
    def send_error(self, msg):
        self.notifications.send_error(msg=msg)

    def to_dict(self):
        return {UserM.USERNAME: self.get_name()}

    def login(self) -> bool:
        raise Exception("Can't login while logged in")

    def logout(self):
        self.logged_user = None
        return True

    def get_name(self, userid=None):
        return self.username

    def appoint_manager(self, sub: Subscribed, shop: Shop, permissions: List[str]):
        session_app = self.get_appointment(shop)
        return session_app.appoint_manager(sub, permissions)

    def appoint_owner(self, new_owner_sub: Subscribed, shop: Shop):
        owner_app = self.get_appointment(shop)
        return owner_app.appoint_owner(new_owner_sub)

    def promote_manager_to_owner(self, manager_sub: Subscribed, shop: Shop):
        session_app: Appointment = self.get_appointment(shop)
        return session_app.promote_manager_to_owner(manager_sub)

    @add_to_session
    def get_appointment(self, shop: Shop):
        if shop in self.appointments:
            return self.appointments[shop]
        raise Exception("no appointment for shop. shop id - ", shop.shop_id)

    def add_product(self, shop: Shop, **product_info) -> Product:
        return self.get_appointment(shop).add_product(**product_info)

    def edit_product(self, shop: Shop, product_id: int, **to_edit):
        return self.get_appointment(shop).edit_product(product_id, **to_edit)

    def delete_product(self, shop: Shop, product_id: int):
        return self.get_appointment(shop).delete_product(product_id)

    def un_appoint_manager(self, unappointed_manager, shop: Shop):
        unappointing_owner_app = self.get_appointment(shop)
        return unappointing_owner_app.un_appoint_manager(unappointed_manager)

    def un_appoint_owner(self, owner_sub, shop: Shop):
        session_app = self.get_appointment(shop)
        return session_app.un_appoint_owner(owner_sub)

    def edit_manager_permissions(self, manager_sub: Subscribed, shop: Shop, permissions: List[str]):
        owner_app = self.get_appointment(shop)
        return owner_app.edit_manager_permissions(manager_sub, permissions)

    # @add_to_session
    def open_shop(self, shop_details):
        new_shop = Shop(**shop_details)
        owner = ShopOwner(new_shop, username=self.username)
        new_shop.founder = self
        new_shop.add_owner(self)
        self.appointments[new_shop] = owner
        return new_shop

    def get_shop_transaction_history(self, shop: Shop):
        app = self.get_appointment(shop)
        return app.get_shop_transaction_history()

    @add_to_session
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        return True

    @add_to_session
    def get_personal_transaction_history(self):
        return self.transactions

    def get_shop_discounts(self, shop: Shop) -> List[Discount]:
        return self.get_appointment(shop).get_discounts()

    def add_discount(self, shop, has_cond, condition, discount) -> Discount:
        appointment = self.get_appointment(shop)
        return appointment.add_discount(has_cond, condition, discount)

    def delete_discounts(self, shop, discount_ids):
        appointment = self.get_appointment(shop)
        return appointment.delete_discounts(discount_ids)

    def aggregate_discounts(self, shop, discount_ids, func) -> bool:
        appointment = self.get_appointment(shop)
        return appointment.aggregate_discounts(discount_ids, func)

    def move_discount_to(self, shop: Shop, src_discount_id: int, dst_discount_id: int) -> bool:
        appointment = self.get_appointment(shop)
        return appointment.move_discount_to(src_discount_id, dst_discount_id)

    def get_shop_purchase_conditions(self, shop: Shop) -> List[Condition]:
        return self.get_appointment(shop).get_purchase_conditions()

    def add_purchase_condition(self, shop: Shop, condition: Condition) -> bool:
        appointment = self.get_appointment(shop)
        return appointment.add_purchase_condition(condition)

    def remove_purchase_condition(self, shop: Shop, condition_id: int) -> bool:
        appointment = self.get_appointment(shop)
        return appointment.remove_purchase_condition(condition_id)

    def get_permissions(self, shop) -> Dict[str, bool]:
        appointment = self.get_appointment(shop)
        if not appointment:
            return super().get_permissions(shop)
        return appointment.get_permissions()

    def get_shop_staff_info(self, shop: Shop) -> List[Appointment]:
        appointment = self.get_appointment(shop)
        return appointment.get_shop_staff_info()

    @add_to_session
    def get_appointments(self):
        return list(self.appointments.values())

    def add_purchase_type(self, shop: Shop, product_id: int, purchase_type_info: dict) -> PurchaseType:
        return self.get_appointment(shop).add_purchase_type(product_id, purchase_type_info)

    def offer_price(self, shop: Shop, product_id: int, offer: float) -> bool:
        return shop.add_price_offer(self.username, product_id, offer)

    def reply_price_offer(self, shop: Shop, product_id: int, offer_maker: str, action: str) -> bool:
        return self.get_appointment(shop).reply_price_offer(product_id, offer_maker, action)

    def get_offers(self, shop: Shop, product_id: int) -> List[PurchaseOffer]:
        return self.get_appointment(shop).get_offers(product_id)


class SystemManager(Subscribed):
    def __init__(self, username: str, system_transactions: TransactionRepo):
        super().__init__(username)
        self.system_transactions = system_transactions

    @add_to_session
    def get_system_transaction_history(self):
        return self.system_transactions.get_transactions()

    @add_to_session
    def get_system_transaction_history_of_shop(self, shop_id: int):
        return self.system_transactions.get_transactions_of_shop(shop_id)

    @add_to_session
    def get_system_transaction_history_of_user(self, username: str):
        return self.system_transactions.get_transactions_of_user(username)
