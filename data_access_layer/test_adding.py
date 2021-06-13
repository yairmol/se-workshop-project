from data_access_layer.purchasing_repository import save_transaction, save_shopping_bag, save_shopping_cart
from data_access_layer.shop_repository import save_shop, remove_shop, get_shop, get_product
from data_access_layer.shop_repository import save_shop
from data_access_layer.subscribed_repository import save_subscribed, get_subscribed, remove_subscribed, \
    remove_all_subscribed
from domain.commerce_system.appointment import ShopOwner, ShopManager
from domain.commerce_system.product import Product, ProductInBag, BuyNow
from domain.commerce_system.shop import Shop
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.product import Product
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session

# subscribed = Subscribed("aviv_the_king6")
# save_subscribed(subscribed, Subscribed)
# remove_subscribed("aviv_the_king6", Subscribed)
# subscribed_from_db = get_subscribed("aviv_the_king5")
# print(subscribed_from_db.username)
# sqlalchemy.orm.exc.UnmappedInstanceError: Class 'domain.commerce_system.user.Subscribed' is not mapped
# print("aviv{}".format(2))
# for i in range(5):
#     subscribed = Subscribed(("aviv{}".format(i)))
#     save_subscribed(subscribed, Subscribed)

# remove_all_subscribed(Subscribed)


# my_shop = Shop("Armani", "Dudu Faruk's favorite shop", "https://website/cool_image.jpg/")
# prod = my_shop.add_product(product_name="Bamba", price=30.5, description="its osem", quantity=10, categories=["snacks"])

# prod_in_bag = ProductInBag(prod, 1, prod.get_purchase_type_of_type(BuyNow))
# save_shop(my_shop)
# # remove_shop(165)
# p = get_product("Bamba")
# s: Shop = get_shop("Armani")
# with Session(engine) as session:
#     session.add(s)
#     print(s.products)
#     print(s.name)
# shop_from_db = get_shop("Armani")
# print(shop_from_db.description)
# shopping_cart = ShoppingCart()
# shopping_cart.add_shopping_bag(ShoppingBag(my_shop))
# shopping_cart.add_to_shopping_bag(my_shop, prod, 5)
# with Session(engine) as session:
#     session.add(shopping_cart)
#     session.commit()
# with Session(engine) as session:
#     session.add(shopping_cart)
#     session.commit()
# shopping_cart.shopping_bags = {shop: shoppingBag}
# save_shopping_cart(shopping_cart)

# save_shopping_bag(shoppingBag)
# subscribed
# shop.foreign_keys.add()

shop = Shop("aviv", "tahles")
shop_id = shop.shop_id

shop2 = Shop("aviv22", "tahles22")
shop_id2 = shop.shop_id

sub4 = Subscribed("yes44")
sub3 = Subscribed("yes33")
sub2 = Subscribed("yes22")
sub = Subscribed("yes")

owner3 = ShopOwner(shop, "yes33", "yes")
owner2 = ShopOwner(shop2, "yes22")
owner1 = ShopOwner(shop, "yes")

owner1.owner_appointees = [owner3]

manager1 = ShopManager(shop2, owner2.username, [], username="yes")
owner_apped2 = ShopManager(shop, owner1.username, [], username="yes22")

manager4 = ShopManager(shop, owner1.username, [], "yes44")

sub4.appointments[shop] = manager4

sub3.appointments[shop] = owner3

sub2.appointments[shop2] = owner2
sub2.appointments[shop] = owner_apped2

sub.appointments[shop2] = manager1

sub.appointments[shop] = owner1

shop.add_manager(manager4)
shop.add_owner(owner3)
shop.add_owner(owner1)
shop2.add_owner(owner2)
shop2.add_manager(manager1)

save_shop(shop)

save_subscribed(sub)
save_subscribed(sub2)
save_subscribed(sub2)
save_subscribed(sub4)

