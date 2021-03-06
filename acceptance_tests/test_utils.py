from enum import Enum, auto
from typing import Tuple, List, Dict, Union

from config.config import config, ConfigFields as cf
from domain.delivery_module.delivery_system import IDeliveryFacade, DeliveryFacadeAlwaysTrue
from domain.payment_module.payment_system import IPaymentsFacade, PaymentsFacadeAlwaysTrue
from test_data import users, shops, permissions, products, payment_details
from service.system_service import SystemService
from data_model import UserModel as Um


def get_credentials(user: dict):
    return {Um.USERNAME: user[Um.USERNAME], Um.PASSWORD: user[Um.PASSWORD]}


def enter_register_and_login(commerce_system: SystemService, user: dict) -> str:
    response = commerce_system.enter()
    assert response["status"] and isinstance(response["result"], str) and response["result"] != ""
    session_id = response["result"]
    assert commerce_system.register(session_id, **user)["status"]
    assert commerce_system.login(session_id, **get_credentials(user))["status"]
    return session_id


def add_product(session_id: str, comm_sys: SystemService, shop: int, product: dict):
    product_id = comm_sys.add_product_to_shop(session_id, shop, **product)['result']
    assert isinstance(product_id, int)
    assert product_id > 0
    return product_id


def register_login_users(commerce_system, num_users) -> Dict[str, dict]:
    return {
        enter_register_and_login(commerce_system, u): u for u in users[:num_users]
    }


def enter_guests(commerce_system: SystemService, num_guests) -> List[str]:
    return [commerce_system.enter()['result'] for _ in range(num_guests)]


def open_shops(commerce_system: SystemService, sessions, num_shops) -> (Dict[int, dict], Dict[int, str]):
    num_users = len(sessions)
    shop_ids_to_sessions_and_shops = {
        commerce_system.open_shop(sessions[i % num_users], **shops[i])['result']: (shops[i], sessions[i % num_users])
        for i in range(num_shops)
    }
    shop_id_to_shop = {sid: shop for sid, (shop, _) in shop_ids_to_sessions_and_shops.items()}
    shop_id_to_session = {sid: session for sid, (_, session) in shop_ids_to_sessions_and_shops.items()}
    shop_ids = list(shop_id_to_session.keys())
    assert all(map(lambda sid: isinstance(sid, int) and sid > 0, shop_ids))
    return shop_id_to_shop, shop_id_to_session


def add_products(commerce_system: SystemService, shop_id_to_sess, shop_ids, num_products):
    num_shops = len(shop_ids)
    pid_to_product_and_sid = {
        add_product(
            shop_id_to_sess[shop_ids[i % num_shops]], commerce_system, shop_ids[i % num_shops], products[i]
        ): (products[i], shop_ids[i % num_shops])
        for i in range(num_products)
    }
    pid_to_product = {pid: product for pid, (product, sid) in pid_to_product_and_sid.items()}
    pid_to_sid = {pid: sid for pid, (product, sid) in pid_to_product_and_sid.items()}
    return pid_to_product, pid_to_sid


def appoint_owners_and_managers(
        commerce_system: SystemService, sessions, sessions_to_users, shop_ids
) -> (Dict[int, str], Dict[int, Tuple[str, List[str]]]):
    """
    appoint an additional owner and manger for every shop in shop_ids
    return 2 dictionaries. the first maps shop id to the appointed owner username.
    the second maps shop id to the  appointed manager username and his permissions
    """
    num_users, num_shops = len(sessions), len(shop_ids)
    shop_owners_dict, shop_managers_dict = {}, {}
    for i in range(num_shops):
        assert commerce_system.appoint_shop_owner(
            sessions[i % num_users], shop_ids[i], users[(i + 1) % num_users]["username"]
        )["status"]
        user_session = [s for s in sessions_to_users.keys() if sessions_to_users[s] == users[(i + 1) % num_users]][0]
        shop_owners_dict[shop_ids[i]] = user_session
        assert commerce_system.appoint_shop_manager(
            sessions[i % num_users], shop_ids[i], users[(i + 2) % num_users]["username"],
            permissions[i % (len(permissions))]
        )["status"]
        user_session = [s for s in sessions_to_users.keys() if sessions_to_users[s] == users[(i + 2) % num_users]][0]
        shop_managers_dict[shop_ids[i]] = (user_session, permissions[i % len(permissions)])
    return shop_owners_dict, shop_managers_dict


def shop_to_products(product_to_shop, shop_ids):
    return {
        shop: [p for p, s in product_to_shop.items() if s == shop]
        for shop in shop_ids
    }


def sessions_to_shops(
        shop_to_openers: Dict[int, str],
        shop_to_owners: Dict[int, str],
        shop_to_managers: Dict[int, Tuple[str, List[str]]],
        sessions: List[str]
):
    shops_to_users = {
        shop: [shop_to_openers[shop], shop_to_owners[shop], shop_to_managers[shop]]
        for shop in shop_to_openers.keys()
    }
    sessions_to_shops_ret: Dict[str, List[int]] = {
        sess: [shop for shop, staff_sessions in shops_to_users.items() if sess in staff_sessions]
        for sess in sessions
    }
    return shops_to_users, sessions_to_shops_ret


def get_shops_not_owned_by_user(user_sess: str, shop_ids: List[int], shop_to_staff: Dict[int, List[str]]):
    return [s for s in shop_ids if user_sess not in shop_to_staff[s]]


def make_purchases(
        commerce_system: SystemService, session: str,
        product_to_shop: Dict[int, int], products_to_buy: List[int]
):
    return all(map(lambda p: commerce_system.purchase_product(
        session, product_to_shop[p], p, 1, payment_details[0], {}
    )["status"], products_to_buy))


def fill_with_data(
        commerce_system: SystemService, num_guests, num_subs, num_shops, num_products
):
    guest_sessions = enter_guests(commerce_system, num_guests)
    sess_to_users = register_login_users(commerce_system, num_subs)
    subs_sessions = list(sess_to_users.keys())
    sid_to_shop, sid_to_sess = open_shops(commerce_system, subs_sessions, num_shops)
    shop_ids = list(sid_to_shop.keys())
    pid_product, pid_to_sid = add_products(commerce_system, sid_to_sess, shop_ids, num_products)
    return guest_sessions, subs_sessions, sid_to_shop, sid_to_sess, pid_to_sid


class PaymentFacadeMocks(Enum):
    ALWAYS_TRUE = auto()
    ALWAYS_FALSE = auto()


class DeliveryFacadeMocks(Enum):
    ALWAYS_TRUE = auto()
    ALWAYS_FALSE = auto()


class PaymentFacadeAlwaysFalse(IPaymentsFacade):

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        return False

    def cancel_payment(self, transaction_id: str) -> bool:
        return True


class DeliveryFacadeAlwaysFalse(IDeliveryFacade):

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        return False

    def cancel_delivery(self, delivery_id: str) -> bool:
        return True


def set_payment_facade(mock_type: PaymentFacadeMocks) -> None:
    facade = IPaymentsFacade.get_payment_facade()
    mock = {
        PaymentFacadeMocks.ALWAYS_FALSE: PaymentFacadeAlwaysFalse,
        PaymentFacadeMocks.ALWAYS_TRUE: PaymentsFacadeAlwaysTrue
    }[mock_type]()
    facade.pay = mock.pay
    facade.cancel_payment = mock.cancel_payment


def set_delivery_facade(mock_type: DeliveryFacadeMocks) -> None:
    facade = IDeliveryFacade.get_delivery_facade()
    mock = {
        DeliveryFacadeMocks.ALWAYS_FALSE: DeliveryFacadeAlwaysFalse,
        DeliveryFacadeMocks.ALWAYS_TRUE: DeliveryFacadeAlwaysTrue
    }[mock_type]()
    facade.deliver_to = mock.deliver_to
    facade.cancel_delivery = mock.cancel_delivery


def reset_facades():
    IPaymentsFacade.reset()
    IDeliveryFacade.reset()


def admin_login(commerce_system: SystemService):
    admin_username = config[cf.ADMIN_CREDENTIALS][cf.ADMIN_USERNAME]
    admin_password = config[cf.ADMIN_CREDENTIALS][cf.ADMIN_PASSWORD]
    admin_session = commerce_system.enter()["result"]
    commerce_system.login(admin_session, admin_username, admin_password)
    return admin_session


class NotificationMock:
    @staticmethod
    def send_message(*args, **kwargs):
        return True

    @staticmethod
    def send_error(*args, **kwargs):
        return True

    @staticmethod
    def send_broadcast(*args, **kwargs):
        return True
