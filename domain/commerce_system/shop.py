class Shop:
    def sell_product(self, product_id: str, payment_details: dict) -> bool:
        raise NotImplementedError()

    def add_product(self, product_details: dict) -> bool:
        raise NotImplementedError()

    def get_shop_info(self) -> str:
        raise NotImplementedError()
