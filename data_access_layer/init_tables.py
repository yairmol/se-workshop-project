from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT, TIME
from sqlalchemy.orm import registry, relationship, backref, polymorphic_union
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.collections import attribute_mapped_collection

from domain.commerce_system.appointment import ShopManager, ShopOwner
from domain.commerce_system.category import Category
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.appointment import ShopManager, ShopOwner
from domain.commerce_system.category import Category
from domain.commerce_system.purchase_conditions import Policy, MaxQuantityForProductCondition, \
    DateWindowForProductCondition, DateWindowForCategoryCondition, TimeWindowForProductCondition, \
    TimeWindowForCategoryCondition, CompositePurchaseCondition, ANDCondition, ORCondition
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product, ProductInBag
from domain.commerce_system.product import Product
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product, ProductInBag
from domain.discount_module.discount_calculator import Discount, Condition, ProductQuantityCondition, \
    CategoryQuantityCondition, SumSimpleCondition, TotalSumCondition, CategorySumCondition, AdditiveDiscount, \
    MaxDiscount, XorDiscount, StoreDiscount, CategoryDiscount, ProductDiscount

# Engine

engine = create_engine('sqlite:///ahla_super.db', echo=True)
meta = MetaData()
mapper_registry = registry()

# Tables

# subscribed = Table(
#     'subscribed',
#     mapper_registry.metadata,
#     Column('username', String, primary_key=True),
# )
#
# transaction = Table(
#     'transaction',
#     mapper_registry.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, ForeignKey("subscribed.username")),
#     Column('shop_id', Integer, ForeignKey("shop.shop_id")),
#     Column('date', DATE),
#     Column('price', FLOAT),
# )

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

# shop_manager_appointments = Table(
#     'shop_manager_appointments',
#     mapper_registry.metadata,
#     Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
#     Column('shop_id', Integer, ForeignKey("shop.id")),
#     Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
#     Column('delete_product', Integer),
#     Column('edit_product', Integer),
#     Column('add_product', Integer),
#     Column('discount', Integer),
#     Column('purchase_condition', Integer),
#     Column('get_trans_history', Integer),
#     Column('get_staff_permission', Integer),
# )
#
# shop_owner_appointments = Table(
#     'shop_owner_appointments',
#     mapper_registry.metadata,
#     Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
#     Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE')),
#     Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
# )

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

purchase_policies = Table(
    'purchase_policies',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
    Column('condition_type', String),
    Column('category', String, ForeignKey('categories.name', ondelete='CASCADE')),
    Column('min_time', TIME),
    Column('max_time', TIME),
    Column('min_date', DATE),
    Column('max_date', DATE),
    Column('product_id', Integer, ForeignKey('products.product_id', ondelete='CASCADE')),
    Column('max_quantity', Integer),
    Column('parent_policy', Integer, ForeignKey('purchase_policies.id', ondelete='CASCADE')),
)


discount_condition = Table(
    'discount_condition',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String),
    Column('minimum', Integer),
    Column('conditioned_product_id', Integer),
    Column('conditioned_category', String),
    Column('parent_condition', Integer, ForeignKey('discount_condition.id', ondelete='CASCADE')),
)

discount = Table(
    'discount',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
    Column('condition', Integer, ForeignKey('discount_conditions.id', ondelete='CASCADE')),
    Column('parent_discount', Integer, ForeignKey('discount.id', ondelete='CASCADE')),

)
#
# composite_discounts = Table(
#     'composite_discounts',
#     mapper_registry.metadata,
#     Column('parent_discount', Integer, ForeignKey('discount.id', ondelete='CASCADE'), primary_key=True),
#     Column('child_discount', Integer, ForeignKey('discount.id', ondelete='CASCADE'), primary_key=True),
# )
#
# composite_discount_conditions = Table(
#     'composite_discount_conditions',
#     mapper_registry.metadata,
#     Column('parent_condition', Integer, ForeignKey('discount_condition.id', ondelete='CASCADE'), primary_key=True),
#     Column('child_condition', Integer, ForeignKey('discount_condition.id', ondelete='CASCADE'), primary_key=True),
# )


# mapper_registry.map_imperatively(Condition, discount_condition)
# mapper_registry.map_imperatively(SimpleCondition, discount_condition)
# mapper_registry.map_imperatively(QuantitySimpleCondition, discount_condition)
# mapper_registry.map_imperatively(ProductQuantityCondition, discount_condition)
# mapper_registry.map_imperatively(CategoryQuantityCondition, discount_condition)
# mapper_registry.map_imperatively(SumSimpleCondition, discount_condition)
# mapper_registry.map_imperatively(TotalSumCondition, discount_condition)
# mapper_registry.map_imperatively(CategorySumCondition, discount_condition)
# mapper_registry.map_imperatively(ANDCondition, discount_condition)
# mapper_registry.map_imperatively(ORCondition, discount_condition)


# mapper_registry.map_imperatively(Discount, discount)
# mapper_registry.map_imperatively(ConditionalDiscount, discount)
# mapper_registry.map_imperatively(ProductDiscount, discount)
# mapper_registry.map_imperatively(CategoryDiscount, discount)
# mapper_registry.map_imperatively(StoreDiscount, discount)
# # mapper_registry.map_imperatively(CompositeDiscount, discount)
# mapper_registry.map_imperatively(XorDiscount, discount)
# mapper_registry.map_imperatively(MaxDiscount, discount)
# mapper_registry.map_imperatively(AdditiveDiscount, discount)

#
# mapper_registry.map_imperatively(Discount, discount, properties={
#     "condition": relationship(Condition)
# })

# mapper_registry.map_imperatively(Subscribed, subscribed, properties={
#     "shoppingBag": relationship(ShoppingBag, backref='subscribed', cascade='all, delete, delete-orphan'),
#     "transactions": relationship(Transaction, backref='subscribed', cascade='all, delete, delete-orphan')
# })
mapper_registry.map_imperatively(Shop, shop, properties={
    "product": relationship(Product, backref='shop', cascade='all, delete, delete-orphan'),
    "shopping_bag": relationship(ShoppingBag, backref='shop', cascade='all, delete, delete-orphan'),
    "conditions": relationship(Policy, backref='shop', cascade='all, delete, delete-orphan')
})
mapper_registry.map_imperatively(Product, product, properties={
    "categories": relationship(Category, backref='product', secondary=categories_product_mtm),
    "policies": relationship(Policy, backref='product', cascade='all, delete, delete-orphan'),
    # "p_time_policies": relationship(TimeWindowForProductCondition, back_populates='time_policy_product',
    #                                 cascade='all, delete, delete-orphan'),
    # "p_date_policies": relationship(DateWindowForProductCondition, back_populates='date_policy_product',
    #                                 cascade='all, delete, delete-orphan')
})
# mapper_registry.map_imperatively(Transaction, transaction)
mapper_registry.map_imperatively(Category, categories, properties={
    "policies": relationship(Policy, backref='categories', cascade='all, delete, delete-orphan')
    # "c_date_policies": relationship(DateWindowForCategoryCondition, back_populates='date_policy_category',
    #                                 cascade='all, delete, delete-orphan')
})
# mapper_registry.map_imperatively(ShopManager, shop_manager_appointments)
# mapper_registry.map_imperatively(ShopOwner, shop_owner_appointments)
# mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
#     "shoppingBags": relationship(ShoppingBag, backref='shopping_cart'),
#     "subscribed": relationship(Subscribed, backref='shopping_cart')
# })
mapper_registry.map_imperatively(ShoppingBag, shopping_bag)

mapper_registry.map_imperatively(
    Policy,
    purchase_policies,
    # properties={
    #     "complex_children": relationship(
    #         Policy,
    #         backref=backref(
    #             'purchase_policies',
    #             remote_side=[purchase_policies.c.id],
    #         )
    #     ),
    #     # "conditioned_product": relationship(Product, backref='purchase_policies'),
    #     # "conditioned_category": relationship(Category, backref='purchase_policies')
    # },
    polymorphic_on=purchase_policies.c.condition_type,

)

mapper_registry.map_imperatively(
    MaxQuantityForProductCondition,
    purchase_policies,
    polymorphic_identity='max_quantity_for_product_condition',
    inherits=Policy,
    # properties={
    #     "max_policy_product": relationship(
    #         Product,
    #         back_populates='policies',
    #         cascade='all, delete'
    #     )
    # }
)

mapper_registry.map_imperatively(
    TimeWindowForCategoryCondition,
    purchase_policies,
    polymorphic_identity='time_window_for_category_condition',
    inherits=Policy,
    # properties={
    #     "time_policy_category": relationship(
    #         Category,
    #         back_populates='policies',
    #         cascade='all, delete'
    #     )
    # }
)

mapper_registry.map_imperatively(
    TimeWindowForProductCondition,
    purchase_policies,
    polymorphic_identity='time_window_for_product_condition',
    inherits=Policy,
    # properties={
    #     "time_policy_product": relationship(
    #         Product,
    #         back_populates='policies',
    #         cascade='all, delete'
    #     )
    # }
)

mapper_registry.map_imperatively(
    DateWindowForCategoryCondition,
    purchase_policies,
    polymorphic_identity="date_window_for_category_condition",
    inherits=Policy,
    # properties={
    #     "date_policy_category": relationship(
    #         Category,
    #         back_populates='policies',
    #         cascade='all, delete'
    #     )
    # }
)

mapper_registry.map_imperatively(
    DateWindowForProductCondition,
    purchase_policies,
    polymorphic_identity="date_window_for_product_condition",
    inherits=Policy,
    # properties={
    #     "date_policy_product": relationship(
    #         Product,
    #         back_populates='policies',
    #         cascade='all, delete'
    #     )
    # }
)

mapper_registry.map_imperatively(
    CompositePurchaseCondition,
    purchase_policies,
    polymorphic_identity="compositeCondition",
    inherits=Policy,
    properties={
        "conditions": relationship(Policy, backref=backref('policies', remote_side=[purchase_policies.c.id]),
                                   cascade='all, delete, delete-orphan')
    }
)

mapper_registry.map_imperatively(
    ANDCondition,
    purchase_policies,
    polymorphic_identity='and_condition',
    inherits=CompositePurchaseCondition,
)

mapper_registry.map_imperatively(
    ORCondition,
    purchase_policies,
    polymorphic_identity='or_condition',
    inherits=CompositePurchaseCondition,
)

# mapper_registry.map_imperatively(ShopManager, shop_manager_appointments)
# mapper_registry.map_imperatively(ShopOwner, shop_owner_appointments)
mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
    "shopping_bags": relationship(ShoppingBag, backref='shopping_cart',
                                  collection_class=attribute_mapped_collection('cart_id')),
    # "subscribed": relationship(Subscribed, backref='shopping_cart')
})
mapper_registry.map_imperatively(ProductInBag, shopping_bag_products)

mapper_registry.metadata.create_all(engine)
