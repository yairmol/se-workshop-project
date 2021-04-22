from typing import List


class IDeliveryFacade:

    def deliver_to(self, products: List[dict], address: str, contact_details: dict) -> bool:
        raise NotImplementedError()


class DeliveryFacadeAlwaysTrue(IDeliveryFacade):

    def deliver_to(self, products: List[dict], address: str, contact_details: dict) -> bool:
        return True
