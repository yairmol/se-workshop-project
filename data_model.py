class UserModel:
    USERNAME = "username"
    PASSWORD = "password"
    EMAIL = "email"


class ShopModel:
    SHOP_NAME = "shop_name"
    SHOP_DESC = "description"
    SHOP_ID = "shop_id"
    SHOP_PRODS = "products"


class ProductModel:
    PRODUCT_ID = "product_id"
    PRODUCT_NAME = "product_name"
    PRICE = "price"
    PRODUCT_DESC = "description"
    QUANTITY = "quantity"
    CATEGORIES = "categories"
    AMOUNT = "amount"  # for ShoppingBag


class TransactionModel:
    SHOP = "shop"
    PRODUCTS = "products"
    DATE = "date"
    PRICE = "price"


class PermissionsModel:
    EDIT_PRODUCT_PERM = "edit_product"
    ADD_PRODUCT_PERM = "add_product"
    DELETE_PRODUCT_PERM = "delete_product"


admin_credentials = {
    UserModel.USERNAME: "admin",
    UserModel.PASSWORD: "admin",
}
