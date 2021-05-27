from data_access_layer.purchasing_repository import save_transaction
from data_access_layer.shop_repository import save_shop
from data_access_layer.subscribed_repository import save_subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session

subscribed = Subscribed("aviv_the_king5")
# save_subscribed(subscribed)

shop = Shop("Armani", "Dudu Faruk's favorite shop", "")
# save_shop(shop)

