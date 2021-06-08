from unittest import TestCase, main

from domain.commerce_system.product import PurchaseOfferType
from domain.commerce_system.user import User, Subscribed
from data_model import PurchaseTypes as Pt

shop_dict = {"shop_name": "s1", "description": "desc"}
product_dict = {"product_name": "p1", "price": 1.5, "description": "prod_desc", "quantity": 5}
offer_purchase_type_dict = {Pt.PURCHASE_TYPE: Pt.OFFER}


class ShopTests(TestCase):
    def setUp(self) -> None:
        self.founder = User()
        self.assertTrue(self.founder.login(Subscribed("u1")))
        self.shop = self.founder.user_state.open_shop(shop_dict)
        self.product = self.shop.add_product(**product_dict)
        self.buyer = User()
        self.assertTrue(self.buyer.login(Subscribed("u2")))
        self.offered_price = 0.75

    def test_open_shop(self):
        self.assertIsNotNone(self.shop)

    def test_add_purchase_type(self):
        self.assertTrue(self.founder.add_purchase_type(
            self.shop, self.product.product_id, offer_purchase_type_dict.copy())
        )
        self.assertEqual(len(self.product.purchase_types), 2)

    def test_make_offer(self):
        self.test_add_purchase_type()
        self.assertTrue(self.buyer.offer_price(self.shop, self.product.product_id, self.offered_price))

    def test_approve_offer(self):
        self.test_make_offer()
        self.assertTrue(self.founder.reply_price_offer(
            self.shop, self.product.product_id, self.buyer.get_name(), "approve"
        ))
        self.assertTrue(self.product.get_price(PurchaseOfferType, offer_maker=self.buyer.get_name()))

    def test_reject_offer(self):
        self.test_make_offer()
        self.assertTrue(self.founder.reply_price_offer(
            self.shop, self.product.product_id, self.buyer.get_name(), "reject"
        ))
        self.assertRaises(AssertionError, self.product.can_purchase, PurchaseOfferType,
                          offer_maker=self.buyer.get_name())


if __name__ == "__main__":
    main()
