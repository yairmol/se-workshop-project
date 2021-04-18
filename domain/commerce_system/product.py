from data_model import ProductModel as Pm


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
            Pm.PRODUCT_ID: self.product_id,
            Pm.PRODUCT_NAME: self.name,
            Pm.PRODUCT_DESC: self.description,
            Pm.PRICE: self.price,
            Pm.QUANTITY: self.quantity,
            Pm.CATEGORIES: self.categories,
        }
