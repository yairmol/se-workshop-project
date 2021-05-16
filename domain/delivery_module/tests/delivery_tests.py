import unittest
from unittest.mock import MagicMock

from domain.delivery_module.delivery_system import DeliveryFacadeWSEP


class TestDelivery(unittest.TestCase):

    def test_success_delivery(self):

        delivery_system = DeliveryFacadeWSEP()
        contact_details = {'name': 'dudu faruk', 'address': 'Rager Blvd 12', 'city': 'Beer Sheva', 'country': 'israel', 'zip': 8458527}
        res = delivery_system.deliver_to(contact_details)
        assert res

    def test_fail_delivery(self):
        delivery_system = DeliveryFacadeWSEP()
        contact_details = {'name': 'dudu faruk'}
        res = delivery_system.deliver_to(contact_details)
        assert not res

    def test_cancel_delivery(self):
        delivery_system = DeliveryFacadeWSEP()
        contact_details = {'name': 'dudu faruk', 'address': 'Rager Blvd 12', 'city': 'Beer Sheva', 'country': 'israel', 'zip': 8458527}
        res = delivery_system.deliver_to(contact_details)
        assert res
        res2 = delivery_system.cancel_delivery(res)
        assert res2



