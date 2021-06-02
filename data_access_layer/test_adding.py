from data_access_layer.purchasing_repository import save_transaction, save_shopping_bag, save_shopping_cart
from data_access_layer.shop_repository import save_shop, remove_shop, get_shop
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from init_tables import engine, shop, shopping_bag
from sqlalchemy.orm import Session

subscribed = Subscribed("aviv_the_king6")
# save_subscribed(subscribed)
# remove_subscribed("aviv_the_king5")
# subscribed_from_db = get_subscribed("aviv_the_king5")
# print(subscribed_from_db.username)


shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
# save_shop(shop)
# # remove_shop(165)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)
shopping_cart = ShoppingCart(1)
shoppingBag = ShoppingBag(shop)
shopping_cart.shopping_bags = {shop: shoppingBag}
save_shopping_cart(shopping_cart)

# save_shopping_bag(shoppingBag)
# subscribed
# shop.foreign_keys.add()
