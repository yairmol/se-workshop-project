# from domain.commerce_system.appointment import Appointment, ShopManager, ShopOwner
# from domain.commerce_system.user import Subscribed
# from init_tables import engine
# from sqlalchemy.orm import Session
#
#
# def save_subscribed(sub: Subscribed):
#     with Session(engine) as session:
#         session.add(sub)
#         session.commit()
#
#
# def get_subscribed(username: str):
#     with Session(engine) as session:
#         subscribed = session.query(Subscribed).filter_by(username=username).first()
#         return subscribed
#
#
# def delete_subscribed(username: str):
#     with Session(engine) as session:
#         subscribed = session.query(Subscribed).filter_by(username=username).first()
#         session.delete(subscribed)
#         session.commit()
#
#
# def update_permissions(manager_username, shop_id, perms_lst):
#     with Session(engine) as session:
#         manager_row = session.query(ShopManager).filter_by(username=manager_username, shop_id=shop_id).first()
#         for perm in ['delete_product_permission', 'edit_product_permission', 'add_product_permission',
#                      'discount_permission', 'purchase_condition_permission', 'get_trans_history_permission',
#                      'get_staff_permission']:
#             manager_row[perm] = perm in perms_lst
#         session.commit()
#
#
# def save_appointment(appointment: Appointment):
#     with Session(engine) as session:
#         session.add(appointment)
#         session.commit()
#
#
# def delete_manager(username, shop_id):
#     delete_appointment(username, shop_id, ShopManager)
#
#
# def delete_owner(username, shop_id):
#     delete_appointment(username, shop_id, ShopOwner)
#
#
# def delete_appointment(username, shop_id, cls):
#     with Session(engine) as session:
#         subscribed = session.query(cls).filter_by(username=username, shop_id=shop_id).first()
#         session.delete(subscribed)
#         session.commit()
#
#
# def promote_manager(manager_username, shop, appointer):
#     delete_manager(manager_username, shop.shop_id)
#     save_appointment(ShopOwner(shop, manager_username, appointer))
#
#
# def get_only_subs():
#     subs = {}
#     with Session(engine) as session:
#         subs_dto = session.query(Subscribed).all()
#         for row in subs_dto:
#             subs[row.username] = Subscribed(row.username)
#         return subs
#
#
# def get_all_owners():
#     owners = {}
#     with Session(engine) as session:
#         owners_dto = session.query(ShopOwner).all()
#         for row in owners_dto:
#             owners[row.username] = ShopOwner(row.shop_id, row.username)
#         for row in owners_dto:
#             appointer = owners[row.appointer]
#             owners[row.username].appointer = appointer
#         return owners
#
#
# def get_all_managers(owners):
#     managers = {}
#     with Session(engine) as session:
#         managers_dto = session.query(ShopManager).all()
#         for row in managers_dto:
#             appointer = owners[row.appointer]
#             owners[row.username].appointer = appointer
#         return managers
#
#
# def get_all_subs(shops):
#     subs = get_only_subs()
#     owners = get_all_owners()
#     managers = get_all_managers(owners)
#     for username, manager in managers:
#         subs[username].appointments[shops[manager.shop_id]] = manager
#     for username, owner in managers:
#         subs[username].appointments[shops[owner.shop_id]] = owner
#     return subs
#
#
# # def construct_permissions(row):
# #     perms_ret = []
# #     for perm in ['delete_product_permission', 'edit_product_permission',
# #                  'add_product_permission', 'discount_permission',
# #                  'purchase_condition_permission', 'get_trans_history_permission',
# #                  'get_staff_permission']:
# #         if row[perm]:
# #             perms_ret += [perm]
# #     return perms_ret
#
# # def get_manager_appointees(appointer, shop_id):
# #     shop = get_shop(shop_id)
# #     manager_appointees = []
# #     with Session(engine) as session:
# #         manager_appointees_dto = session.query(ShopManager).filter_by(appointer=appointer, shop_id=shop_id).all()
# #         for row in manager_appointees_dto:
# #             manager_appointees += [ShopManager(shop, appointer, construct_permissions(row), row.username)]
# #         return manager_appointees
# #
# #
# # def get_owner_appointees(appointer, shop_id):
# #     shop = get_shop(shop_id)
# #     owner_appointees = []
# #     with Session(engine) as session:
# #         manager_appointees_dto = session.query(ShopManager).filter_by(appointer=appointer, shop_id=shop_id).all()
# #         for row in manager_appointees_dto:
# #             manager_appointees += [ShopManager(shop, appointer, construct_permissions(row), row.username)]
# #         return manager_appointees
