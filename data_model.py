class UserModel:
    USERNAME = "username"
    PASSWORD = "password"
    EMAIL = "email"


class ShopModel:
    SHOP_NAME = "shop_name"
    SHOP_DESC = "description"
    SHOP_ID = "shop_id"
    SHOP_IMAGE = "shopImage"
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


class ConditionsModel:
    MAX_QUANTITY = "max_quantity"
    PRODUCT = "product"
    CATEGORY = "category"
    MIN_TIME = "min_time"
    MAX_TIME = "max_time"
    MIN_DATE = "min_date"
    MAX_DATE = "max_date"
    MAX_QUANTITY_FOR_PRODUCT = "MaxQuantityForProductCondition"
    TIME_WINDOW_FOR_CATEGORY = "TimeWindowForCategoryCondition"
    TIME_WINDOW_FOR_PRODUCT = "TimeWindowForProductCondition"
    DATE_WINDOW_FOR_CATEGORY = "DateWindowForCategoryCondition"
    DATE_WINDOW_FOR_PRODUCT = "DateWindowForProductCondition"


admin_credentials = {
    UserModel.USERNAME: "admin",
    UserModel.PASSWORD: "admin-password",
}
