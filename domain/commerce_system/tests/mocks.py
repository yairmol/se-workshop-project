from typing import Union, List

from domain.delivery_module.delivery_system import IDeliveryFacade
from domain.notifications.notifications import INotifications
from domain.payment_module.payment_system import IPaymentsFacade


class PaymentMock(IPaymentsFacade):

    def __init__(self, payment_works: bool):
        self.pay_called = False
        self.pay_cancelled = False
        self.payment_works = payment_works

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        self.pay_called = True
        if self.payment_works:
            return str(hash(tuple(payment_details.items())))
        return False

    def cancel_payment(self, payment_id: str) -> bool:
        self.pay_cancelled = True
        return True


class DeliveryMock(IDeliveryFacade):

    def __init__(self, delivery_works: bool):
        self.delivery_called = False
        self.delivery_cancelled = False
        self.delivery_works = delivery_works

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        self.delivery_called = True
        if self.delivery_works:
            return str(hash(frozenset(contact_details.items())))
        return False

    def cancel_delivery(self, delivery_id: str) -> bool:
        self.delivery_cancelled = True
        return True


class NotificationMock:
    @staticmethod
    def send_message(*args, **kwargs):
        return True

    @staticmethod
    def send_error(*args, **kwargs):
        return True

    @staticmethod
    def send_broadcast(*args, **kwargs):
        return True
