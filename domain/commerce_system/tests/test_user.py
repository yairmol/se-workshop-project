import unittest
from datetime import datetime
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.tests.mocks import DeliveryMock, PaymentMock
from domain.commerce_system.user import User
from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.payment_module.payment_system import IPaymentsFacade


class TestCommerceSystemFacade(unittest.TestCase):

    def setUp(self) -> None:
        self.facade = CommerceSystemFacade(Authenticator())

    def test_add_active_user1(self):
        self.facade.enter()
        self.facade.enter()
        assert len(self.facade.active_users) == 2

    def test_user_register1(self):
        uid = self.facade.enter()
        sub = self.facade.register(uid, "aviv", "123456")
        assert len(self.facade.registered_users) == 1


class UserTests(unittest.TestCase):
    def setUp(self) -> None:
        IPaymentsFacade.get_payment_facade = lambda: PaymentMock(True)
        IDeliveryFacade.get_delivery_facade = lambda: DeliveryMock(True)

    users = [
        ["username", "password"],
        ["username2", "password2"],
    ]

    shops = [
        {"shop_name": "shop1"}
    ]

    products = [
        {"product_name": "p1", "quantity": 1, "price": 20}
    ]

    payment_details = [
        {"credit_number": "0000-0000-0000-0000", "cvv": 000, "expiration_date": datetime(year=2024, month=6, day=1)}
    ]

    delivery_details = {}

    @staticmethod
    def register_and_login(username, password):
        user = User()
        sub = user.register(username, password=password)
        user.login(sub)
        return user

    def open_shop(self):
        u = self.register_and_login(*self.users[1])
        shop = u.user_state.open_shop(self.shops[0])
        prod = u.user_state.add_product(shop, **self.products[0])
        return shop, prod

    def test_get_transactions_empty(self):
        user = self.register_and_login(*self.users[0])
        self.assertEqual(user.get_personal_transactions_history(), [])

    def test_get_transactions(self):
        user = self.register_and_login(*self.users[0])
        shop, prod = self.open_shop()
        self.assertTrue(user.purchase_product(shop, prod, 1, self.payment_details[0], self.delivery_details))
        transactions = user.get_personal_transactions_history()
        self.assertEqual(len(transactions), 1)

    def test_get_transactions_by_guest(self):
        user = User()
        self.assertRaises(Exception, user.get_personal_transactions_history)
