import json
from typing import List, Union

from domain.discount_module.discount_management import SimpleCond, DiscountDict, CompositeDiscountDict


def enter(user_id) -> dict:
    return {
        "action": "enter",
        "user": user_id,
        "params": {}
    }


def exit(user_id) -> dict:
    return {
        "action": "exit",
        "user": user_id,
        "params": {}
    }


def register(token: str, username: str, password: str, **more) -> dict:
    return {
        "action": "register",
        "user": token,
        "params": {
            "username": username, "password": password
        }
    }


def login(token: str, username: str, password: str) -> dict:
    return {
        "action": "login",
        "user": token,
        "params": {"username": username, "password": password}
    }


def save_product_to_cart(token: str, shop_ref: Union[str, int], product_ref: Union[str, int], amount_to_buy: int) -> dict:
    return {
        "action": "save_product_to_cart",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_id={"ref": product_ref},
            amount_to_buy=amount_to_buy)
    }


def remove_product_from_cart(token: str, shop_ref: Union[str, int], product_ref: Union[str, int], amount: int) -> dict:
    return {
        "action": "remove_product_from_cart",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_id={"ref": product_ref},
            amount=amount)
    }


def purchase_product(token: str, shop_ref: Union[str, int], product_ref: Union[str, int], amount_to_buy: int, payment_details: dict,
                     delivery_details: dict, add_ref=None) -> dict:
    ret = {
        "action": "purchase_product",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_id={"ref": product_ref},
            amount_to_buy=amount_to_buy,
            payment_details=payment_details,
            delivery_details=delivery_details
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def purchase_shopping_bag(token: str, shop_ref: int, payment_details: dict, delivery_details: dict,
                          add_ref=None) -> dict:
    ret = {
        "action": "purchase_shopping_bag",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            payment_details=payment_details,
            delivery_details=delivery_details
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def purchase_cart(token: str, payment_details: dict, delivery_details: dict, add_ref=None) -> dict:
    ret = {
        "action": "purchase_cart",
        "user": token,
        "params": dict(
            payment_details=payment_details,
            delivery_details=delivery_details
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def logout(token: str) -> dict:
    return {
        "action": "logout",
        "user": token,
        "params": dict()
    }


def open_shop(token: str, shop_name, description, add_ref=None) -> dict:
    ret = {
        "action": "open_shop",
        "user": token,
        "params": dict(
            shop_name=shop_name,
            description=description,
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def add_product_to_shop(token: str, shop_ref: Union[str, int], product_name, description, price,
                        quantity, categories: list, add_ref=None) -> dict:
    ret = {
        "action": "add_product_to_shop",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_name=product_name,
            description=description,
            price=price,
            quantity=quantity,
            categories=categories
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def edit_product_info(token: str, shop_ref: Union[str, int], product_ref: Union[str, int], product_name: str = None,
                      description: str = None, price: float = None, quantity: int = None,
                      categories: List[str] = None) -> dict:
    return {
        "action": "edit_product_info",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_id={"ref": product_ref},
            product_name=product_name,
            description=description,
            price=price,
            quantity=quantity,
            categories=categories
        )
    }


def delete_product(token: str, shop_ref: Union[str, int], product_ref: Union[str, int]) -> dict:
    return {
        "action": "delete_product",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            product_id={"ref": product_ref},
        )
    }


def add_purchase_condition(token: str, shop_ref: Union[str, int], add_ref=None, **condition_dict):
    ret = {
        "action": "add_purchase_condition",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            **condition_dict
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def remove_purchase_condition(token: str, shop_ref: Union[str, int], condition_ref: Union[str, int]):
    return {
        "action": "remove_purchase_condition",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            condition_id={"ref": condition_ref}
        )
    }


def appoint_shop_manager(token: str, shop_ref: Union[str, int], username: str, permissions: List[str]) -> dict:
    return {
        "action": "appoint_shop_manager",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
            permissions=permissions
        )
    }


def appoint_shop_owner(token: str, shop_ref: Union[str, int], username: str) -> dict:
    return {
        "action": "appoint_shop_owner",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
        )
    }


def promote_shop_owner(token: str, shop_ref: Union[str, int], username: str) -> dict:
    return {
        "action": "promote_shop_owner",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
        )
    }


def edit_manager_permissions(token: str, shop_ref: Union[str, int], username: str, permissions: List[str]) -> dict:
    return {
        "action": "edit_manager_permissions",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
            permissions=permissions
        )
    }


def un_appoint_manager(token: str, shop_ref: Union[str, int], username: str) -> dict:
    return {
        "action": "un_appoint_manager",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
        )
    }


def un_appoint_shop_owner(token: str, shop_ref: Union[str, int], username: str) -> dict:
    return {
        "action": "un_appoint_shop_owner",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            username=username,
        )
    }


def add_discount(token: str, shop_ref: Union[str, int], has_cond: bool, condition: List[Union[str, SimpleCond, List]],
                 discount: Union[DiscountDict, CompositeDiscountDict], add_ref=None) -> dict:
    ret = {
        "action": "add_discount",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            has_cond=has_cond,
            condition=condition,
            discount=discount
        )
    }
    if add_ref:
        ret["ref_id"] = add_ref
    return ret


def aggregate_discounts(token: str, shop_ref: Union[str, int], discount_refs: List[Union[int, str]], operator: str):
    return {
        "action": "aggregate_discounts",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            discount_ids=[
                {"ref", ref} for ref in discount_refs
            ],
            operator=operator,
        )
    }


def move_discount_to(token: str, shop_ref: Union[str, int], src_discount_ref: Union[str, int], dst_discount_ref: Union[str, int]):
    return {
        "action": "move_discount_to",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            src_discount_id={"ref": src_discount_ref},
            dst_discount_id={"ref": dst_discount_ref},
        )
    }


def delete_discounts(token: str, shop_ref: Union[str, int], discount_refs: List[Union[str, int]]):
    return {
        "action": "delete_discounts",
        "user": token,
        "params": dict(
            shop_id={"ref": shop_ref},
            discount_ids=[
                {"ref", ref} for ref in discount_refs
            ],
        )
    }


def generate_init(path: str, users: list, *actions):
    with open(path, "w+") as f:
        json.dump({
            "users": users,
            "actions": actions
        }, f)
