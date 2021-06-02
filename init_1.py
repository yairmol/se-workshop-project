import init_generator as ig
from data_model import PermissionsModel as Perms
ig.generate_init(
    "init_generated.json",
    ["u1", "u2"],
    ig.enter("u1"),
    ig.enter("u2"),
    ig.register("u1", "user1", "password"),
    ig.register("u2", "user2", "password"),
    ig.login("u1", "user1", "password"),
    # ig.login("u2", "user2", "password"),
    ig.open_shop("u1", "shop1", "one and only shop", add_ref="s1"),
    ig.add_product_to_shop("u1", "s1", "Bamba", "its osem", 20, 30, ["snacks"], add_ref="p1"),
    ig.appoint_shop_manager("u1", "s1", "user2", [
        Perms.DELETE_PRODUCT_PERM, Perms.EDIT_PRODUCT_PERM, Perms.ADD_PRODUCT_PERM
    ]),
    # ig.logout("u2")
)