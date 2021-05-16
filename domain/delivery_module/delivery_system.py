from __future__ import annotations
from typing import List, Union
import json
import requests
from requests import Timeout


class IDeliveryFacade:

    @staticmethod
    def get_delivery_facade() -> IDeliveryFacade:
        return DeliveryFacadeAlwaysTrue()

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
    url = 'https://cs-bgu-wsep.herokuapp.com/'

    def handshake(self) -> bool:
        data = {"action_type": "handshake"}
        try:
            response = requests.post(self.url, data, timeout=5)
            return response.text == 'OK'
        except Timeout:
            return False

    def deliver_to(self, contact_details: dict = None) -> Union[str, bool]:
        if self.handshake():
            data = {"action_type": "supply"}
            data.update(contact_details)
            try:
                response = requests.post(self.url, data, timeout=5)
                if response.text == '-1':
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
                return response.text == '1'
            except Timeout:
                return False
        return False
