from unittest import TestCase, main

from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop


shop_dict = {"shop_name": "s1", "description": "desc"}
product_dict = {"product_name": "p1", "price": 1.5, "description": "prod_desc", "quantity": 5}


class ShopTests(TestCase):
    pass
    # TODO: ADD TESTS HERE!!


if __name__ == "__main__":
    main()
