import unittest
from unittest.mock import MagicMock

from domain.payment_module.payment_system import PaymentsFacadeWSEP
import responses
import requests


class TestPayment(unittest.TestCase):
    url = 'https://cs-bgu-wsep.herokuapp.com/'

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.ERROR = '-1'
        # self.responses.add(...)

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def test_success_handshake_and_success_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body='12345', status=200,
            content_type='application/json')
        payment_details = {'card_number': '1234567890', 'month': '4', 'year': '2021', 'holder': 'dudu faruk',
                           'ccv': '222', 'id': '20444444'}
        resp = payment_system.pay(100, payment_details)
        assert resp

    def test_success_handshake_and_fail_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body=self.ERROR, status=200,
            content_type='application/json')
        payment_details = {'card_number': '1234567890', 'month': '4', 'year': '2021', 'holder': 'dudu faruk',
                           'ccv': '222', 'id': '20444444'}

        resp = payment_system.pay(100, payment_details)
        assert not resp

    def test_fail_handshake_and_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_system.handshake = MagicMock(return_value=False)
        self.responses.add(
            responses.POST, self.url,
            body='12345', status=200,
            content_type='application/json')
        payment_details = {'card_number': '1234567890', 'month': '4', 'year': '2021', 'holder': 'dudu faruk',
                           'ccv': '222', 'id': '20444444'}

        resp = payment_system.pay(100, payment_details)
        assert not resp

    def test_success_cancel_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body='1', status=200,
            content_type='application/json')
        trans_id = '1'
        resp = payment_system.cancel_payment(trans_id)
        assert resp

    def test_fail_cancel_pay(self):
        payment_system = PaymentsFacadeWSEP()
        payment_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body='-1', status=200,
            content_type='application/json')
        trans_id = '1'
        resp = payment_system.cancel_payment(trans_id)
        assert not resp
