class Shop:

    def __init__(self, shop_name):
        self.shop_name = shop_name
        # to expand

    def sell_product(self, product_id: str, payment_details: dict) -> bool:
        raise NotImplementedError()

    def add_product(self, product_details: dict) -> bool:
        raise NotImplementedError()

    def get_shop_info(self) -> str:
        raise NotImplementedError()
