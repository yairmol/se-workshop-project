from unittest import TestCase, main

from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop


shop_dict = {"shop_name": "s1", "description": "desc"}
product_dict = {"product_name": "p1", "price": 1.5, "description": "prod_desc", "quantity": 5}


class ShopTests(TestCase):

    SHOP_ID = 1
    PROD_ID = 1

    def test_get_shop_dict(self):
        my_shop_dict = shop_dict.copy()
        shop = Shop(**shop_dict)
        p = shop.add_product(**product_dict)
        my_product_dict = product_dict.copy()
        my_product_dict["product_id"] = p.product_id
        my_shop_dict["shop_id"] = shop.shop_id
        my_shop_dict["products"] = [my_product_dict]
        self.assertEqual(my_shop_dict, shop.to_dict())

    def test_get_shop_info(self):
        facade = CommerceSystemFacade()
        facade.shops[self.SHOP_ID] = Shop(**shop_dict)
        my_shop_dict = shop_dict.copy()
        my_shop_dict["shop_id"] = self.SHOP_ID
        my_shop_dict["products"] = []
        self.assertEquals(facade.get_shop_info(self.SHOP_ID), my_shop_dict)


if __name__ == "__main__":
    main()
