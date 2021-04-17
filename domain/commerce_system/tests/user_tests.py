import unittest
from datetime import datetime
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.user import User, Subscribed


class TestCommerceSystemFacade(unittest.TestCase):

    def test_add_active_user1(self):

        facade = CommerceSystemFacade()
        facade.enter()
        assert len(facade.active_users) == 1

    def test_user_register1(self):
        user = User()
        try:
            sub = user.register("aviv", "123456")
            print(type(sub))
            assert isinstance(sub, Subscribed)
        except Exception as e:
            assert False

    def test_user_register2(self):
        user = User()
        user.user_state = Subscribed("aviv", "123456")
        try:
            sub = user.register("aviv", "123456")
            assert False
        except Exception as e:
            assert True


class UserTests(unittest.TestCase):

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

    @staticmethod
    def register_and_login(username, password):
        user = User()
        user.register(username, password)
        user.login(username, password)
        return user

    def open_shop(self):
        u = self.register_and_login(*self.users[1])
        shop = u.open_shop(**self.shops[0])
        prod = u.add_product(shop, **self.products[0])
        return shop, prod

    def test_get_transactions_empty(self):
        user = self.register_and_login(*self.users[0])
        self.assertEquals(user.get_personal_transactions_history(), [])

    def test_get_transactions(self):
        user = self.register_and_login(*self.users[0])
        shop, prod = self.open_shop()
        self.assertTrue(user.buy_product(shop, prod, 1, **self.payment_details[0]))
        transactions = user.get_personal_transactions_history()
        self.assertEquals(len(transactions), 1)

    def test_get_transactions_by_guest(self):
        user = User()
        self.assertRaises(Exception, user.get_personal_transactions_history)
