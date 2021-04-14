from acceptance_tests.test_data import users, shops, permissions
from domain.commerce_system.facade import ICommerceSystemFacade


def enter_register_and_login(commerce_system: ICommerceSystemFacade, user: dict) -> str:
    session_id = commerce_system.enter()
    assert isinstance(session_id, str) and session_id != ""
    assert commerce_system.register(session_id, **user)
    assert commerce_system.login(session_id, **user["credentials"])
    return session_id


def add_product(session_id: str, comm_sys: ICommerceSystemFacade, shop: str, product: dict):
    product_id = comm_sys.add_product_to_shop(
        session_id, shop, **product
    )
    assert isinstance(product_id, str) and product_id != ""
    return product_id


def fill_system_with_data(
        commerce_system: ICommerceSystemFacade, num_users: int,
        num_shops: int, num_products: int
) -> (dict, dict, dict, dict, dict, dict):
    sessions_to_users = {
        enter_register_and_login(commerce_system, u): u for u in users[:num_users]
    }
    sessions = list(sessions_to_users.keys())
    shop_ids_to_sessions_and_shops = {
        commerce_system.open_shop(sessions[i % num_users], **shops[i]): (shops[i], sessions[i % num_users])
        for i in range(num_shops)
    }
    shop_id_to_shop = {sid: shop for sid, (shop, _) in shop_ids_to_sessions_and_shops.items()}
    shop_id_to_session = {sid: session for sid, (_, session) in shop_ids_to_sessions_and_shops.items()}
    shop_ids = list(shop_id_to_session.keys())
    assert all(map(lambda sid: isinstance(sid, str) and sid != "", shop_ids))
    product_ids_to_shop_ids = {
        commerce_system.add_product_to_shop(
            sessions[(i % num_shops) % num_users], shop_ids[i % num_shops]
        ): shop_ids[i % num_shops]
        for i in range(num_products)
    }
    assert all(map(lambda pid: isinstance(pid, str) and pid != "", product_ids_to_shop_ids.keys()))
    shop_managers_dict, shop_owners_dict = {}, {}
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
    return (sessions_to_users, shop_id_to_shop, shop_id_to_session,
            product_ids_to_shop_ids, shop_owners_dict, shop_managers_dict)
