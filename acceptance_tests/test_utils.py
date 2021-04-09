from commerce_system.facade import ICommerceSystemFacade


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
):
    pass
