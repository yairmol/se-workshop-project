from typing import List, Union


class IDeliveryFacade:

    def deliver_to(self, products: List[dict], address: str, contact_details: dict) -> Union[str, bool]:
        """
        :param products:
        :param address:
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

    def deliver_to(self, products: List[dict], address: str, contact_details: dict) -> Union[str, bool]:
        DeliveryFacadeAlwaysTrue.__delivery_id += 1
        return str(DeliveryFacadeAlwaysTrue.__delivery_id)

    def cancel_delivery(self, delivery_id: str) -> bool:
        return True
