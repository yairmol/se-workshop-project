from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT, Boolean
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

# from domain.authentication_module.authenticator import Password
from domain.commerce_system.appointment import ShopManager, ShopOwner, Appointment
from domain.commerce_system.category import Category
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product, ProductInBag
from data_access_layer.engine import engine, mapper_registry, meta

# Engine



# Tables

subscribed = Table(
    'subscribed',
    mapper_registry.metadata,
    Column('username', String, primary_key=True),
)

passwords = Table(
    'password',
    mapper_registry.metadata,
    Column('username', String, ForeignKey("subscribed.username"), primary_key=True),
    Column('password_hash', String),
    Column('salt', String),
)

# TODO: save the transaction's products
transaction = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, ForeignKey("subscribed.username")),
    Column('shop_id', Integer, ForeignKey("shop.shop_id")),
    Column('date', DATE),
    Column('price', FLOAT),
)

shop = Table(
    'shop',
    mapper_registry.metadata,
    Column('shop_id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('image_url', String),
)

categories_product_mtm = Table(
    'product_categories_mtm',
    mapper_registry.metadata,
    Column('product_category_id', Integer, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
    Column('product_id', Integer, ForeignKey("products.product_id", ondelete='CASCADE')),
)

product = Table(
    'products',
    mapper_registry.metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('price', Integer),
    Column('description', String),
    Column('quantity', Integer),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
)

categories = Table(
    'categories',
    mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True),
    Column('name', String),
)


appointments = Table(
    'appointments',
    mapper_registry.metadata,
    Column('username', String, ForeignKey("subscribed.username"), primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.shop_id"), primary_key=True),
    Column('appointer_username', String, ForeignKey("appointments.username"), nullable=True),
    Column('delete_product_permission', Boolean),
    Column('edit_product_permission', Boolean),
    Column('add_product_permission', Boolean),
    Column('discount_permission', Boolean),
    Column('purchase_condition_permission', Boolean),
    Column('get_trans_history_permission', Boolean),
    Column('get_staff_permission', Boolean),
    Column('type', String)
)

shopping_cart = Table(
    'shopping_cart',
    mapper_registry.metadata,
    Column('cart_id', Integer, primary_key=True),
    # Column('username', String, ForeignKey('subscribed.name')),
)

shopping_bag = Table(
    'shopping_bag',
    mapper_registry.metadata,
    Column('bag_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.shop_id", ondelete='CASCADE')),
    Column('cart_id', String, ForeignKey("shopping_cart.cart_id", ondelete="CASCADE")),
)

shopping_bag_products = Table(
    'shopping_bag_products',
    mapper_registry.metadata,
    Column('bag_id', Integer, ForeignKey("shopping_bag.bag_id", ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey("products.product_id"), nullable=False),
    Column('amount', Integer)
)

# Mappings

mapper_registry.map_imperatively(Subscribed, subscribed, properties={
    "transactions": relationship(Transaction, backref='subscribed'),
    "appointments": relationship(Appointment, backref='subscribed',
                                 collection_class=attribute_mapped_collection('shop')),
})

# mapper_registry.map_imperatively(Password, passwords)

mapper_registry.map_imperatively(Shop, shop, properties={
    "products": relationship(Product, backref='shop', collection_class=attribute_mapped_collection('product_id')),
    "shopping_bag": relationship(ShoppingBag, backref='shop'),
    "transactions_history": relationship(Transaction, backref='shop'),
    "shop_managers": relationship(Appointment,
                                  collection_class=attribute_mapped_collection('username')),
    "shop_owners": relationship(Appointment,
                                collection_class=attribute_mapped_collection('username')),
})

mapper_registry.map_imperatively(Product, product, properties={
    "categories": relationship(Category, backref='products', secondary=categories_product_mtm)
})

mapper_registry.map_imperatively(Transaction, transaction)

mapper_registry.map_imperatively(Category, categories)

mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
    "shopping_bags": relationship(
        ShoppingBag, backref='shopping_cart', collection_class=attribute_mapped_collection('shop'),lazy="joined"
    ),
    # "subscribed": relationship(Subscribed, backref='shopping_cart')
})

mapper_registry.map_imperatively(ProductInBag, shopping_bag_products, properties={
    "product": relationship(Product)
})

mapper_registry.map_imperatively(ShoppingBag, shopping_bag, properties={
    "products": relationship(ProductInBag, backref='shopping_bag_products',
                             collection_class=attribute_mapped_collection('product'), lazy="joined"),
    # "shop": relationship(Shop, backref='shop'),
})

mapper_registry.map_imperatively(Appointment, appointments, polymorphic_on='type', properties={
    "shop": relationship(Shop),
})

mapper_registry.map_imperatively(ShopOwner, appointments, polymorphic_identity='O', inherits=Appointment, properties={
    "owner_appointees": relationship(Appointment),
    "manager_appointees": relationship(Appointment),
})

mapper_registry.map_imperatively(ShopManager, appointments, polymorphic_identity='M', inherits=Appointment)

mapper_registry.metadata.create_all(engine)
