class Product:
    def __init__(self, name: str, base_price: float, description: str, quantity: int):
        self.name = name
        self.price = base_price
        self.description = description
        self.quantity = quantity
