from typing import Union


class IPaymentsFacade:

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None) -> Union[str, bool]:
        """
        make a payment
        :param total_price:
        :param payment_details:
        :param contact_details:
        :return: payment id (str) on success else False
        """
        raise NotImplementedError()

    def cancel_payment(self, payment_id: str) -> bool:
        """
        cancel payment identified by payment_id
        :param payment_id:
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
