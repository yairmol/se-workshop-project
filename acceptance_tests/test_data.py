from datetime import datetime

from data_model import (
    UserModel as Um, ShopModel as Sm, ProductModel as Pm, PermissionsModel as PermM,
    ConditionsModel as Cm
)

users = [
    {
        Um.USERNAME: "user1", Um.PASSWORD: "password", "email": "email@gmail.com",
    },
    {
        Um.USERNAME: "user2", Um.PASSWORD: "password", "email": "email2@gmail.com",
    },
    {
        Um.USERNAME: "user3", Um.PASSWORD: "password", "email": "email3@gmail.com",
    },
    {
        Um.USERNAME: "user4", Um.PASSWORD: "password", "email": "email4@gmail.com",
    },
    {
        Um.USERNAME: "user5", Um.PASSWORD: "password", "email": "email5@gmail.com",
    }
]

shops = [
    {Sm.SHOP_NAME: "shop1", Sm.SHOP_DESC: "shop1 desc"},
    {Sm.SHOP_NAME: "shop2", Sm.SHOP_DESC: "shop2 desc"},
    {Sm.SHOP_NAME: "shop3", Sm.SHOP_DESC: "shop3 desc"},
    {Sm.SHOP_NAME: "shop4", Sm.SHOP_DESC: "shop4 desc"},
]

categories = [
    "c1", "c2", "c3", "c4"
]

products = [
    {Pm.PRODUCT_NAME: "p1", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 1, Pm.QUANTITY: 10, Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p2", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 2.5, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p3", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 1.25, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p4", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 10, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p5", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 32, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p6", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 200, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p7", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 250, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p8", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 8999.99, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p9", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 47, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p10", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 96, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p11", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 1220, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
    {Pm.PRODUCT_NAME: "p12", Pm.PRODUCT_DESC: "a product", Pm.PRICE: 3, Pm.QUANTITY: 10,
     Pm.CATEGORIES: categories[0:1]},
]

admin_credentials = {
    Um.USERNAME: "admin", Um.PASSWORD: "admin"
}

permissions = [
    [PermM.ADD_PRODUCT_PERM, PermM.EDIT_PRODUCT_PERM, PermM.DELETE_PRODUCT_PERM],
    [PermM.ADD_PRODUCT_PERM, PermM.EDIT_PRODUCT_PERM],
    [PermM.DELETE_PRODUCT_PERM]
]

simple_condition_dict = {
    Cm.CONDITION_TYPE: Cm.DATE_WINDOW_FOR_CATEGORY, Cm.MIN_DATE: '1/5/2021', Cm.MAX_DATE: '20/7/2021',
    Cm.CATEGORY: "c1"
}

payment_details = [
    {
        "credit_card_number": "4580-1111-1111-1111",
        "expiration_date": int(datetime(year=2024, month=6, day=1).timestamp()),
        "card_holder_name": "Ligma"
    }
]

delivery_details = {}
