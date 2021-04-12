class Product:
    def __init__(self, product_id: str, name: str, base_price: float, description: str):
        self.product_id = product_id
        self.name = name
        self.price = base_price
        self.description = description

    def sell_product(self):
        raise NotImplementedError()

    def add_products(self, amount):
        raise NotImplementedError()
