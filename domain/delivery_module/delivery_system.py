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


class DeliveryFacadeWSEP(IDeliveryFacade):
    url = config[cf.DELIVERY_SYSTEM_URL]
    SUCCESSFUL_HANDSHAKE = 'OK'
    SUCCESSFUL_DELIVERY_CANCEL = '1'
    ERROR = '-1'

    def handshake(self) -> bool:
        data = {"action_type": "handshake"}
        try:
            response = requests.post(self.url, data, timeout=5)
            return response.text == self.SUCCESSFUL_HANDSHAKE
        except Timeout:
            return False

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        if self.handshake():
            data = {"action_type": "supply"}
            data.update(contact_details)
            try:
                response = requests.post(self.url, data, timeout=5)
                if response.text == self.ERROR:
                    return False
                return response.text
            except Timeout:
                return False
        return False

    def cancel_delivery(self, delivery_id: str) -> bool:
        if self.handshake():
            data = {"action_type": "cancel_pay", "transaction_id": delivery_id}
            try:
                response = requests.post(self.url, data, timeout=5)
                return response.text == self.SUCCESSFUL_DELIVERY_CANCEL
            except Timeout:
                return False
        return False
