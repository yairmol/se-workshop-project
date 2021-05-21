from __future__ import annotations
from typing import Union
import json
import requests
from requests import Timeout

from config.config import config, ConfigFields as cf


class IPaymentsFacade:

    __instance = None

    @staticmethod
    def payment_facade_from_config():
        if config[cf.PAYMENT_FACADE] == "real":
            return PaymentsFacadeWSEP()
        elif config[cf.PAYMENT_FACADE] == "always_true":
            return PaymentsFacadeAlwaysTrue()

    @staticmethod
    def get_payment_facade() -> IPaymentsFacade:
        if not IPaymentsFacade.__instance:
            IPaymentsFacade.__instance = IPaymentsFacade.payment_facade_from_config()
        return IPaymentsFacade.__instance

    def cancel_payment(self, transaction_id: str) -> bool:
        """
        cancel payment identified by payment_id
        :param transaction_id:
        :return: True on success, otherwise False
        """
        raise NotImplementedError()

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        """
        make a payment
        :param total_price:
        :param payment_details:
        :param contact_details:
        :return: payment id (str) on success else False
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
    url = config[cf.PAYMENT_SYSTEM_URL]
    SUCCESSFUL_HANDSHAKE = 'OK'
    SUCCESSFUL_PAY_CANCEL = '1'
    ERROR = '-1'

    def handshake(self) -> bool:
        data = {"action_type": "handshake"}
        try:
            response = requests.post(self.url, data, timeout=5)
            return response.text == self.SUCCESSFUL_HANDSHAKE
        except Timeout:
            return False

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        if self.handshake():
            data = {"action_type": "pay"}
            data.update(payment_details)
            try:
                response = requests.post(self.url, data, timeout=5)
                if response.text == self.ERROR:
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
                return response.text == self.SUCCESSFUL_PAY_CANCEL
            except Timeout:
                return False
        return False
