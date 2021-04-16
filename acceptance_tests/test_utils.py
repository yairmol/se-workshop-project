from typing import Tuple, List, Dict

from acceptance_tests.test_data import users, shops, permissions
from service.system_service import SystemService


def enter_register_and_login(commerce_system: SystemService, user: dict) -> str:
    session_id = commerce_system.enter()
    assert isinstance(session_id, str) and session_id != ""
    assert commerce_system.register(session_id, **user)
    assert commerce_system.login(session_id, **user["credentials"])
    return session_id


def add_product(session_id: str, comm_sys: SystemService, shop: str, product: dict):
    product_id = comm_sys.add_product_to_shop(
        session_id, shop, **product
    )
    assert isinstance(product_id, str) and product_id != ""
    return product_id


def register_login_users(commerce_system, num_users) -> Dict[str, dict]:
    return {
        enter_register_and_login(commerce_system, u): u for u in users[:num_users]
    }


def open_shops(commerce_system, sessions, num_shops) -> (Dict[str, dict], Dict[str, str]):
    num_users = len(sessions)
    shop_ids_to_sessions_and_shops = {
        commerce_system.open_shop(sessions[i % num_users], **shops[i]): (shops[i], sessions[i % num_users])
        for i in range(num_shops)
    }
    shop_id_to_shop = {sid: shop for sid, (shop, _) in shop_ids_to_sessions_and_shops.items()}
    shop_id_to_session = {sid: session for sid, (_, session) in shop_ids_to_sessions_and_shops.items()}
    shop_ids = list(shop_id_to_session.keys())
    assert all(map(lambda sid: isinstance(sid, str) and sid != "", shop_ids))
    return shop_id_to_shop, shop_id_to_session


def add_products(commerce_system, sessions, shop_ids, num_products):
    num_users, num_shops = len(sessions), len(shop_ids)
    product_ids_to_shop_ids = {
        commerce_system.add_product_to_shop(
            sessions[(i % num_shops) % num_users], shop_ids[i % num_shops]
        ): shop_ids[i % num_shops]
        for i in range(num_products)
    }
    assert all(map(lambda pid: isinstance(pid, str) and pid != "", product_ids_to_shop_ids.keys()))
    return product_ids_to_shop_ids


def appoint_owners_and_managers(
        commerce_system, sessions, sessions_to_users, shop_ids
) -> (Dict[str, str], Dict[str, Tuple[str, List[str]]]):
    num_users, num_shops = len(sessions), len(shop_ids)
    shop_owners_dict, shop_managers_dict = {}, {}
    for i in range(num_shops):
        assert commerce_system.appoint_shop_owner(
            sessions[i % num_users], shop_ids[i], users[(i + 1) % num_users]["username"]
        )
        user_session = [s for s in sessions_to_users.keys() if sessions_to_users[s] == users[(i + 1) % num_users]][0]
        shop_owners_dict[shop_ids[i]] = user_session
        assert commerce_system.appoint_shop_manager(
            sessions[i % num_users], shop_ids[i], users[(i + 2) % num_users]["username"],
            permissions[i % (len(permissions))]
        )
        user_session = [s for s in sessions_to_users.keys() if sessions_to_users[s] == users[(i + 2) % num_users]][0]
        shop_managers_dict[shop_ids[i]] = (user_session, permissions[i % len(permissions)])
    return shop_owners_dict, shop_managers_dict


def shop_to_products(product_to_shop, shop_ids):
    return {
        shop: [p for p, s in product_to_shop.items() if s == shop]
        for shop in shop_ids
    }


def sessions_to_shops(
        shop_to_openers: Dict[str, str],
        shop_to_owners: Dict[str, str],
        shop_to_managers: Dict[str, Tuple[str, List[str, str]]],
        sessions: List[str]
):
    shops_to_users = shop_to_openers
    shops_to_users.update(shop_to_owners)
    shops_to_users.update({s: m for s, (m, p) in shop_to_managers.items()})
    return shops_to_users, {
        sess: [shop for shop, sess2 in shops_to_users if sess == sess2]
        for sess in sessions
    }


def get_shop_not_owned_by_user(user, shop_ids, shop_to_staff):
    return [s for s in shop_ids if user not in shop_to_staff[s]][0]


def make_purchases(
        commerce_system: SystemService, session: str, shop_id: str, products: List[str]
) -> List[str]:
    products_purchased = list()
    for product_id in products:
        assert commerce_system.purchase_product(session, shop_id, product_id)
        products_purchased.append(product_id)
    return products_purchased
