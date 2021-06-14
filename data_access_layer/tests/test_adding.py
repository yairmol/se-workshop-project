from data_access_layer.engine import engine
from data_access_layer.purchasing_repository import save_transaction
# from data_access_layer.shop_repository import save_shop, remove_shop, get_shop, save_product, remove_product, \
#     save_policy, remove_policy, save_category, remove_category, remove_x
from data_access_layer.shop_repository import save, get_first
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed
from domain.commerce_system.category import Category
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import MaxQuantityForProductCondition, TimeWindowForCategoryCondition, \
    TimeWindowForProductCondition, DateWindowForCategoryCondition, DateWindowForProductCondition, ANDPolicy
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from data_model import ConditionsModel as CondM
# from init_tables import engine
from sqlalchemy.orm import Session

# subscribed = Subscribed("aviv_the_king5")
# save_subscribed(subscribed)
# remove_subscribed("aviv_the_king5")
# subscribed_from_db = get_subscribed("aviv_the_king5")
# print(subscribed_from_db.username)
# category = Category("c")
from domain.discount_module.discount_calculator import TotalSumCondition, ProductDiscount, ORCondition
from domain.discount_module.discount_management import SimpleCond, DiscountDict

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
condition_dict2 = {CondM.MIN_TIME: '00:00', CondM.MAX_TIME: '23:59', CondM.CATEGORY: "c", CondM.CONDITION_TYPE: CondM.TIME_WINDOW_FOR_CATEGORY}
condition_dict3 = {CondM.MIN_TIME: '00:00', CondM.MAX_TIME: '23:59', CondM.PRODUCT: product_id, CondM.CONDITION_TYPE: CondM.TIME_WINDOW_FOR_PRODUCT}
condition_dict4 = {CondM.MIN_DATE: '1/5/2021', CondM.MAX_DATE: '30/7/2021', CondM.CATEGORY: "c", CondM.CONDITION_TYPE: CondM.DATE_WINDOW_FOR_CATEGORY}
condition_dict5 = {CondM.MIN_DATE: '1/5/2021', CondM.MAX_DATE: '30/7/2021', CondM.PRODUCT: product_id, CondM.CONDITION_TYPE: CondM.DATE_WINDOW_FOR_PRODUCT}

policy1 = MaxQuantityForProductCondition(condition_dict)
policy2 = TimeWindowForCategoryCondition(condition_dict2)
policy3 = TimeWindowForProductCondition(condition_dict3)
policy4 = DateWindowForCategoryCondition(condition_dict4)
policy5 = DateWindowForProductCondition(condition_dict5)

and_condition_dict = {CondM.CONDITIONS: [policy1, policy2, policy3, policy4, policy5],
CondM.CONDITION_TYPE: CondM.AND}

and_policy = ANDPolicy(and_condition_dict)

product1_discount_dict1: DiscountDict = {
    'type': 'product', 'identifier': 1, 'percentage': 20, "composite": False
}
simple_cond: SimpleCond = {'condition': 'sum', 'type': 'shop', 'identifier': 'shop', 'num': 50}
condition = [simple_cond]

shop.add_discount(True, condition, product1_discount_dict1)


# shop.add_purchase_condition(policy1)
# shop.add_purchase_condition(policy2)
# shop.add_purchase_condition(policy3)
# shop.add_purchase_condition(policy4)
# shop.add_purchase_condition(policy5)

shop.add_purchase_condition(and_policy)

# print(policy.id)
# print(policy.product_id)

save(shop)
# save_product(product)
# save_category(category)
# save_policy(policy1)
# save_policy(policy2)
# save_policy(policy3)
# save_policy(policy4)
# save_policy(policy5)
# save_policy(and_policy)
shop_check = get_first(Shop, name='Armani')
with Session(engine) as session:
    session.add(shop_check)
    print(shop_check.conditions[0].to_dict())

# remove_x(and_policy)
# remove_product(1)
# remove_shop(1)
# remove_category(1)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)
