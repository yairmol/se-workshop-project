import unittest
from unittest.mock import MagicMock

from domain.payment_module.payment_system import PaymentsFacadeWSEP


class TestPayment(unittest.TestCase):

    def test_success_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_details = {'card_number': '1234567890', 'month': '4', 'year': '2021', 'holder': 'dudu faruk',
                           'ccv': '222', 'id': '20444444'}
        res = payment_system.pay(100, payment_details)
        assert res

    def test_fail_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_details = {}
        res = payment_system.pay(100, payment_details)
        assert not res

    def test_cancel_pay(self):
        payment_system = PaymentsFacadeWSEP()
        res = payment_system.cancel_payment('1')
        assert res
