from data_access_layer.engine import get_first, save, delete_all_rows_from_tables
from data_access_layer.purchasing_repository import save_transaction, save_shopping_bag, save_shopping_cart
from data_access_layer.shop_repository import save_shop, remove_shop, get_shop, get_product
from data_access_layer.shop_repository import save_shop
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed, \
    remove_all_subscribed
# from domain.commerce_system.product import Product, ProductInBag, BuyNow
# from domain.commerce_system.shop import Shop
# from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
# from domain.commerce_system.transaction import Transaction
from domain.commerce_system.product import Product, ProductInBag, BuyNow
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session

# subscribed = Subscribed("aviv_the_king6")
# save_subscribed(subscribed, Subscribed)
# remove_subscribed("aviv_the_king6", Subscribed)
# subscribed_from_db = get_subscribed("aviv_the_king6")
# print(subscribed_from_db.username)
# print("aviv{}".format(2))
# for i in range(5):
#     subscribed = Subscribed(("aviv{}".format(i)))
#     save_subscribed(subscribed, Subscribed)

# remove_all_subscribed(Subscribed)

sub = Subscribed("aviv")
sub.open_shop({"shop_name": "shop1", "description": "the one and only shop in the entire commerce system"})
# my_shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
my_shop = sub.open_shop({"shop_name": "shop1", "description": "the one and only shop in the entire commerce system"})
# prod = my_shop.add_product(product_name="Bamba", price=30.5, description="its osem", quantity=10, categories=["snacks"])
#
# prod_in_bag = ProductInBag(prod, 1, prod.get_purchase_type_of_type(BuyNow))
# save(sub)
# u = get_first(Subscribed, username=sub.username)
# print(u.username)

# drop_tables()
# delete_all_rows_from_tables()

# save(my_shop)
# # remove_shop(165)
# u = get_first(Subscribed)
# p = get_first(Product, product_name="Bamba")
# s: Shop = get_first(Shop, name="Armani")
# with Session(engine) as session:
#     session.add(u)
#     session.add(s)
#     print("printing 1: %s" % u.username)
#     print("printing 1: %s" % s.products)
#     print("printing 1: %s" % s.name)
# print("printing 2: %s" % u.username)
# print("printing 2: %s" % s.products)
# print("printing 2: %s" % s.name)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)

# my_shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
# shopping_cart = ShoppingCart()
# shopping_cart.add_shopping_bag(ShoppingBag(my_shop))
# shopping_cart.add_to_shopping_bag(my_shop, prod, 5)
# save(shopping_cart)
#
# c = get_first(ShoppingCart, cart_id=1)
# p = get_first(Product, product_name="Bamba")
# b = get_first(ShoppingBag, bag_id="1")
# with Session(engine) as session:
#     session.add(c)
    # session.add(b)
    # session.commit()

    # print("printing: ", c.shopping_bags)
# print("printing: ", p.product_name)
# print("printing: ", b.products)


# with Session(engine) as session:
#     session.add(shopping_cart)
#     session.commit()
# shopping_cart.shopping_bags = {shop: shoppingBag}
# save_shopping_cart(shopping_cart)

# save_shopping_bag(shoppingBag)
# subscribed
# shop.foreign_keys.add()

