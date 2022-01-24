from typing import TypedDict


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
    SHOP_ID = "shop_id"
    PURCHASE_TYPES = "purchase_types"
    PURCHASE_TYPE = "purchase_type"
    PURCHASE_PRICE = "purchase_price"


class TransactionModel:
    SHOP = "shop"
    PRODUCTS = "products"
    DATE = "date"
    PRICE = "price"


class PermissionsModel:
    EDIT_PRODUCT_PERM = "edit_product"
    ADD_PRODUCT_PERM = "add_product"
    DELETE_PRODUCT_PERM = "delete_product"
    MANAGE_DISCOUNT_PERM = "manage_discounts"
    WATCH_TRANSACTIONS_PERM = "watch_transactions"
    WATCH_STAFF_PERM = "watch_staff"
    MANAGE_PURCHASE_CONDITIONS = "manage_purchase_condition"
    PURCHASE_TYPES_PERM = "purchase_types"


class ConditionsModel:
    CONDITION_TYPE = "condition_type"
    MAX_QUANTITY = "max_quantity"
    PRODUCT = "product"
    CATEGORY = "category"
    MIN_TIME = "min_time"
    MAX_TIME = "max_time"
    MIN_DATE = "min_date"
    MAX_DATE = "max_date"
    CONDITIONS = "conditions"  # for composite conditions
    AND = "and_condition"
    OR = "or_condition"
    MAX_QUANTITY_FOR_PRODUCT = "max_quantity_for_product_condition"
    TIME_WINDOW_FOR_CATEGORY = "time_window_for_category_condition"
    TIME_WINDOW_FOR_PRODUCT = "time_window_for_product_condition"
    DATE_WINDOW_FOR_CATEGORY = "date_window_for_category_condition"
    DATE_WINDOW_FOR_PRODUCT = "date_window_for_product_condition"
    TIME_FORMAT = "%H:%M"
    DATE_FORMAT = "%d/%m/%Y"


class AppointmentModel:
    WORKER_NAME = "username"
    WORKER_TITLE = "title"
    WORKER_APPOINTER = "appointer"
    PERMISSIONS = "permissions"


class PurchaseTypes:
    BUY_NOW = "buy_now"
    OFFER = "offer"
    PURCHASE_TYPE = "purchase_type"
    APPROVE = "approve"
    REJECT = "reject"
    COUNTER = "counter"
    FOR_SUBS_ONLY = "for_subs_only"
    OFFER_MAKER = "offer_maker"
    STATE = "offer_state"


class PurchaseTypeDict(TypedDict):
    purchase_type: str


admin_credentials = {
    UserModel.USERNAME: "admin",
    UserModel.PASSWORD: "admin-password",
}
