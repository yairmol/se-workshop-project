from data_access_layer.purchasing_repository import save_transaction
from data_access_layer.shop_repository import save_shop, remove_shop, get_shop
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session

subscribed = Subscribed("aviv_the_king5")
# save_subscribed(subscribed)
# remove_subscribed("aviv_the_king5")
# subscribed_from_db = get_subscribed("aviv_the_king5")
# print(subscribed_from_db.username)


shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
# save_shop(shop)
# remove_shop(1)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)
