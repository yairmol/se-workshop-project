class IPaymentsFacade:

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None):
        raise NotImplementedError()


class PaymentsFacadeAlwaysTrue(IPaymentsFacade):

    def pay(self, total_price: int, payment_details: dict, contact_details: dict = None):
        return True
