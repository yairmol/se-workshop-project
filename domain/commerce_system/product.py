PRODUCT_ID = "product_id"
PRODUCT_NAME = "product_name"
PRICE = "price"
PRODUCT_DESC = "description"
QUANTITY = "quantity"
CATEGORIES = "categories"


class Product:
    def __init__(self, product_id: int, product_name: str, price: float, description: str, quantity: int, categories):
        if categories is None:
            categories = []
        self.product_id = product_id
        self.name = product_name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.categories = categories

    def to_dict(self):
        return {
            PRODUCT_ID: self.product_id,
            PRODUCT_NAME: self.name,
            PRODUCT_DESC: self.description,
            PRICE: self.price,
            QUANTITY: self.quantity,
            CATEGORIES: self.categories,
        }
