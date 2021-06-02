from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product

engine = create_engine('sqlite:///ahla_super.db', echo=True)
meta = MetaData()
mapper_registry = registry()

subscribed = Table(
    'subscribed',
    mapper_registry.metadata,
    Column('username', String, primary_key=True),
)

# TODO: save the transaction's products
transaction = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('shop_id', Integer),
    Column('date', DATE),
    Column('price', FLOAT),
)

shops = Table(
    'shops',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('image_url', String),
)

products = Table(
    'products',
    mapper_registry.metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('price', Integer),
    Column('description', String),
    Column('quantity', Integer),
    Column('shop_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
)
categories = Table(
    'categories',
    mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True),
    Column('category', String),
)

categories_product_mtm = Table(
    'product_categories_mtm',
    mapper_registry.metadata,
    Column('product_category_id', Integer, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
    Column('product_id', Integer, ForeignKey("products.product_id", ondelete='CASCADE')),
)

shop_manager_appointments = Table(
    'shop_manager_appointments',
    mapper_registry.metadata,
    Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.id")),
    Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
    Column('delete_product', Integer),
    Column('edit_product', Integer),
    Column('add_product', Integer),
    Column('discount', Integer),
    Column('purchase_condition', Integer),
    Column('get_trans_history', Integer),
    Column('get_staff_permission', Integer),
)

shop_owner_appointments = Table(
    'shop_owner_appointments',
    mapper_registry.metadata,
    Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE')),
    Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),

)
shopping_cart = Table(
    'shopping_cart',
    mapper_registry.metadata,
    Column('cart_id', Integer, primary_key=True),
    Column('username', String, ForeignKey("subscribed.username", ondelete='CASCADE'))
)
shopping_bag = Table(
    'shopping_bag',
    mapper_registry.metadata,
    Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE'), primary_key=True),
    Column('cart_id', Integer, ForeignKey("shopping_cart.cart_id", ondelete='CASCADE')),
    Column('product_id', Integer, ForeignKey("products.product_id", ondelete='CASCADE'))
)
purchase_policies = Table(
    'purchase_policies',
    mapper_registry.metadata,
    Column('policy_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shops.id', ondelete='CASCADE')),
    Column('condition_type', String),
    Column('max_quantity', Integer),
    Column('product', Integer, ForeignKey('products.product_id', ondelete='CASCADE')),
    # Column('category', String), TODO: check if category is string or integer
    Column('min_time', String),
    Column('max_time', String),
    Column('min_date', String),
    Column('max_date', String),
    Column('conditions', list),

)

discounts = Table(
    'discounts',
    mapper_registry.metadata,
    Column('discount_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shops.id', ondelete='CASCADE')),
    # Column('Condition', ) TODO
)

# appointments = Table(
#     'appointments',
#     mapper_registry.metadata,
#     Column(ForeignKey("subscribed.username"), primary_key=True),
#     Column(ForeignKey("shop.id")),
#     Column(ForeignKey("subscribed.username")),
# )

mapper_registry.map_imperatively(Subscribed, subscribed)
mapper_registry.map_imperatively(Shop, shops)
mapper_registry.map_imperatively(Product, products)
mapper_registry.map_imperatively(Transaction, transaction)

mapper_registry.metadata.create_all(engine)
