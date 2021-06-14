from __future__ import annotations
from typing import Union
import requests
from requests import Timeout

from config.config import config, ConfigFields as cf


class IDeliveryFacade:

    __instance = None

    @staticmethod
    def delivery_facade_from_config():
        if config[cf.PAYMENT_FACADE] == "real":
            return DeliveryFacadeWSEP()
        elif config[cf.PAYMENT_FACADE] == "always_true":
            return DeliveryFacadeAlwaysTrue()

    @staticmethod
    def get_delivery_facade() -> IDeliveryFacade:
        if not IDeliveryFacade.__instance:
            IDeliveryFacade.__instance = IDeliveryFacade.delivery_facade_from_config()
        return IDeliveryFacade.__instance

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        """
        :param contact_details:
        :return: delivery id (str) in case of success, else False
        """
        raise NotImplementedError()

    def cancel_delivery(self, delivery_id: str) -> bool:
        """
        cancels delivery
        :param delivery_id:
        :return: True on success
        """
        raise NotImplementedError()


class DeliveryFacadeAlwaysTrue(IDeliveryFacade):
    __delivery_id = 0

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        DeliveryFacadeAlwaysTrue.__delivery_id += 1
        return str(DeliveryFacadeAlwaysTrue.__delivery_id)

    def cancel_delivery(self, delivery_id: str) -> bool:
        return True


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_valid_transaction_id(value: int):
    return 10000 <= value <= 100000


class DeliveryFacadeWSEP(IDeliveryFacade):
    SUCCESSFUL_HANDSHAKE = 'OK'
    SUCCESSFUL_DELIVERY_CANCEL = '1'
    ERROR = '-1'
    DELIVERY_FIELDS = {"name", "address", "city", "country", "zip"}

    def handshake(self) -> bool:
        data = {"action_type": "handshake"}
        try:
            response = requests.post(config[cf.DELIVERY_SYSTEM_URL], json=data, timeout=5)
            return response.text == self.SUCCESSFUL_HANDSHAKE
        except Timeout:
            return False

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        if self.handshake():
            data = {"action_type": "supply"}
            data.update(contact_details)
            if not self.DELIVERY_FIELDS.issubset(set(contact_details.keys())):
                return False
            try:
                response = requests.post(config[cf.DELIVERY_SYSTEM_URL], json=data, timeout=5)
                text = response.text
                if represents_int(text):
                    value = int(text)
                    if is_valid_transaction_id(value):
                        return text
                    return False
                return False
            except Timeout:
                return False
        return False

    def cancel_delivery(self, delivery_id: str) -> bool:
        if self.handshake():
            data = {"action_type": "cancel_supply", "transaction_id": delivery_id}
            try:
                response = requests.post(config[cf.DELIVERY_SYSTEM_URL], json=data, timeout=5)
                return response.text == self.SUCCESSFUL_DELIVERY_CANCEL
            except Timeout:
                return False
        return False
