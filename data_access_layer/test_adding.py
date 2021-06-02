from data_access_layer.purchasing_repository import save_transaction
from data_access_layer.shop_repository import save_shop, remove_shop, get_shop, save_product, remove_product, \
    save_policy, remove_policy, save_category, remove_category
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed
from domain.commerce_system.category import Category
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from data_model import ConditionsModel as CondM
from init_tables import engine
from sqlalchemy.orm import Session

# subscribed = Subscribed("aviv_the_king5")
# save_subscribed(subscribed)
# remove_subscribed("aviv_the_king5")
# subscribed_from_db = get_subscribed("aviv_the_king5")
# print(subscribed_from_db.username)
# category = Category("c")
shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
product_dict = {
    "product_name": "p1",
    "price": 1.5,
    "description": "prod_desc",
    "quantity": 5,
    "categories": ['c']
}

product = shop.add_product(**product_dict)
product_id = product.product_id
category = product.categories[0]
# print(category.)
print("ggggggggggggggggggggggg",product_id)

# condition_dict = {
#     CondM.MAX_QUANTITY: 5,
#     CondM.PRODUCT: product_id,
#     CondM.CONDITION_TYPE: CondM.MAX_QUANTITY_FOR_PRODUCT
# }

condition_dict = {CondM.MAX_QUANTITY: 5, CondM.PRODUCT: product_id, CondM.CONDITION_TYPE: CondM.MAX_QUANTITY_FOR_PRODUCT}
policy = MaxQuantityForProductCondition(condition_dict)
print(policy.id)
print(policy.product_id)

# save_shop(shop)
# save_product(product)
# save_category(category)
# save_policy(policy)

# remove_policy(1)
# remove_product(1)
remove_shop(1)
# remove_category(1)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)
