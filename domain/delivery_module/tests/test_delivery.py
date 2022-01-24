import unittest
from unittest.mock import MagicMock

import responses

from domain.delivery_module.delivery_system import DeliveryFacadeWSEP


class TestDelivery(unittest.TestCase):
    url = 'https://cs-bgu-wsep.herokuapp.com/'

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.ERROR = '-1'
        self.SUCCESS = '1'

        # self.responses.add(...)

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def test_success_handshake(self):
        delivery_system = DeliveryFacadeWSEP()
        self.responses.add(responses.POST, self.url,
                           body='OK', status=200)
        res = delivery_system.handshake()
        self.assertTrue(res)

    def test_fail_handshake(self):
        delivery_system = DeliveryFacadeWSEP()
        self.responses.add(responses.POST, self.url,
                           json={'error': 'not found'}, status=404)
        res = delivery_system.handshake()
        self.assertFalse(res)

    def test_success_handshake_and_success_delivery(self):
        delivery_id = '12345'
        delivery_system = DeliveryFacadeWSEP()
        delivery_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body=delivery_id, status=200,
            content_type='application/json')

        contact_details = {'name': 'dudu faruk', 'address': 'Rager Blvd 12', 'city': 'Beer Sheva', 'country': 'israel',
                           'zip': 8458527}
        res = delivery_system.deliver_to(contact_details)
        self.assertEqual(res, delivery_id)

    def test_success_handshake_and_fail_delivery(self):
        delivery_system = DeliveryFacadeWSEP()
        delivery_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body=self.ERROR, status=200,
            content_type='application/json')

        contact_details = {'name': 'dudu faruk', 'address': 'Rager Blvd 12', 'city': 'Beer Sheva', 'country': 'israel',
                           'zip': 8458527}
        res = delivery_system.deliver_to(contact_details)
        self.assertFalse(res)

    def test_fail_handshake_and_delivery(self):
        delivery_system = DeliveryFacadeWSEP()
        delivery_system.handshake = MagicMock(return_value=False)
        self.responses.add(
            responses.POST, self.url,
            body='12345', status=200,
            content_type='application/json')

        contact_details = {'name': 'dudu faruk', 'address': 'Rager Blvd 12', 'city': 'Beer Sheva', 'country': 'israel',
                           'zip': 8458527}
        res = delivery_system.deliver_to(contact_details)
        self.assertFalse(res)

    def test_success_cancel_delivery(self):
        delivery_id = '1'
        delivery_system = DeliveryFacadeWSEP()
        delivery_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body=self.SUCCESS, status=200,
            content_type='application/json')

        res = delivery_system.cancel_delivery(delivery_id)
        self.assertTrue(res)

    def test_fail_cancel_delivery(self):
        delivery_system = DeliveryFacadeWSEP()
        delivery_system.handshake = MagicMock(return_value=True)
        self.responses.add(
            responses.POST, self.url,
            body=self.ERROR, status=200,
            content_type='application/json')

        delivery_id = '1'
        res = delivery_system.cancel_delivery(delivery_id)
        self.assertFalse(res)
