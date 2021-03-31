from unittest import TestCase
from driver import Driver


class GuestTests(TestCase):

    def __init__(self):
        super().__init__()
        self.commerce_system = Driver.get_commerce_system_facade()
