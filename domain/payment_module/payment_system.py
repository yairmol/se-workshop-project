from __future__ import annotations
from typing import Union
import json
import requests
from requests import Timeout


class IPaymentsFacade:

    @staticmethod
    def get_payment_facade() -> IPaymentsFacade:
        return PaymentsFacadeAlwaysTrue()

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        """
        make a payment
        :param total_price:
        :param payment_details:
        :param contact_details:
        :return: payment id (str) on success else False
        """
        raise NotImplementedError()

    def cancel_payment(self, transaction_id: str) -> bool:
        """
        cancel payment identified by payment_id
        :param transaction_id:
        :return: True on success, otherwise False
        """
        raise NotImplementedError()


class PaymentsFacadeAlwaysTrue(IPaymentsFacade):
    __payment_id = 0

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        PaymentsFacadeAlwaysTrue.__payment_id += 1
        return str(PaymentsFacadeAlwaysTrue.__payment_id)

    def cancel_payment(self, payment_id: str) -> bool:
        return True


class PaymentsFacadeWSEP(IPaymentsFacade):
    url = 'https://cs-bgu-wsep.herokuapp.com/'

    def handshake(self) -> bool:
        data = {"action_type": "handshake"}
        try:
            response = requests.post(self.url, data, timeout=5)
            return response.text == 'OK'
        except Timeout:
            return False

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        if self.handshake():
            data = {"action_type": "pay"}
            data.update(payment_details)
            try:
                response = requests.post(self.url, data, timeout=5)
                if response.text == '-1':
                    return False
                return response.text
            except Timeout:
                return False
        return False

    def cancel_payment(self, transaction_id: str) -> bool:
        if self.handshake():
            data = {"action_type": "cancel_pay", "transaction_id": transaction_id}
            try:
                response = requests.post(self.url, data, timeout=5)
                return response.text == '1'
            except Timeout:
                return False
        return False
