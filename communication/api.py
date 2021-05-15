import json
from typing import List, Union

from flask import Flask, request, jsonify
from flask_cors import CORS

from acceptance_tests.test_data import products
from acceptance_tests.test_utils import fill_with_data, make_purchases
from domain.discount_module.discount_management import SimpleCond, DiscountDict
from service.system_service import SystemService


def create_app():
    app = Flask(__name__)
    CORS(app)

    CORS(app, resources={
        r"/.*": {
            "origins": "*",
            "Content-Type": "application/json"
        }
    })
    app.config['CORS_HEADERS'] = 'Content-Type'

    API_BASE = '/api'

    __system_service = SystemService.get_system_service()
    guest_sess, subs_sess, sids_to_shop, sid_to_sess, pid_to_sid = fill_with_data(__system_service, 0, 2, 2, 6)
    make_purchases(__system_service, subs_sess[0], pid_to_sid, list(pid_to_sid.keys())[:3])

    def apply_request_on_function(func, *args, **kwargs):
        print(request.data)
        data = json.loads(request.data)
        return func(*args, **kwargs, **data)

    # 2.1
    @app.route(f'{API_BASE}/validate_token')
    def is_valid_token() -> dict:
        return {
            "is_valid": __system_service.is_valid_token(request.args.get("token"))
        }

    # 2.1
    @app.route(f'{API_BASE}/enter', methods=['POST'])
    def enter() -> dict:
        return __system_service.enter()

    # 2.2
    @app.route(f'{API_BASE}/exit', methods=['DELETE'])
    def exit_():
        return apply_request_on_function(__system_service.exit)

    # 2.3
    @app.route(f'{API_BASE}/register', methods=['POST'])
    def register() -> dict:
        return apply_request_on_function(__system_service.register)

    # 2.4
    @app.route(f'{API_BASE}/login', methods=["POST"])
    def login() -> dict:
        print("login", request.remote_user, "addr", request.remote_addr, request.environ.get('REMOTE_PORT'))
        return apply_request_on_function(__system_service.login)

    @app.route(f'{API_BASE}/userData', methods=["GET"])
    def get_user_data() -> dict:
        return apply_request_on_function(__system_service.get_user_data)

    # 2.5
    @app.route(f'{API_BASE}/shops/<int:shop_id>')
    def get_shop_info(shop_id: int) -> dict:
        return __system_service.get_shop_info(token=request.args.get("token"), shop_id=shop_id)

    @app.route(f'{API_BASE}/all_shops', methods=["GET"])
    def get_all_shop_info() -> dict:
        return __system_service.get_all_shops_info(request.args.get("token"))

    @app.route(f'{API_BASE}/all_user_names/', methods=["GET"])
    def get_all_user_names() -> dict:
        return __system_service.get_all_user_names(request.args.get("token"))

    @app.route(f'{API_BASE}/all_shops_ids_and_names/', methods=["GET"])
    def get_all_shops_ids_and_names() -> dict:
        return __system_service.get_all_ids_and_names(request.args.get("token"))

    # 2.6
    @app.route(f'{API_BASE}/search', methods=["PUT"])
    def search_products() -> List[dict]:
        return apply_request_on_function(__system_service.search_products)

    @app.route(f'{API_BASE}/allCategories', methods=["GET"])
    def get_all_categories() -> List[str]:
        return __system_service.get_all_categories(request.args.get("token"))

    # 2.7
    # TODO: decide on route
    @app.route(f'{API_BASE}/cart/<int:shop_id>/<int:product_id>', methods=['POST'])
    def save_product_to_cart(shop_id: int, product_id: int) -> dict:
        return apply_request_on_function(
                __system_service.save_product_to_cart,
                shop_id=shop_id, product_id=product_id
            )

    # 2.8
    @app.route(f'{API_BASE}/cart')
    def get_cart_info() -> dict:
        return __system_service.get_cart_info(request.args.get("token"))

    # 2.8
    @app.route(f'{API_BASE}/cart/<int:shop_id>/<int:product_id>', methods=['DELETE'])
    def remove_product_from_cart(shop_id: int, product_id: int) -> dict:
        return apply_request_on_function(
                __system_service.remove_product_from_cart,
                shop_id=shop_id, product_id=product_id
            )

    # 2.9
    @app.route(f'{API_BASE}/cart/<int:shop_id>/<int:product_id>', methods=['POST'])
    def purchase_product(shop_id: int, product_id: int) -> dict:
        return apply_request_on_function(
            __system_service.purchase_product,
            shop_id=shop_id, product_id=product_id
        )

    # 2.9
    @app.route(f'{API_BASE}/cart/<int:shop_id>', methods=['POST'])
    def purchase_shopping_bag(shop_id: int) -> dict:
        return apply_request_on_function(
            __system_service.purchase_shopping_bag, shop_id=shop_id
        )

    # 2.9
    @app.route(f'{API_BASE}/cart', methods=['POST'])
    def purchase_cart() -> dict:
        return apply_request_on_function(__system_service.purchase_cart)

    # 3. Subscriber Requirements

    # 3.1
    @app.route(f'{API_BASE}/logout', methods=['PUT'])
    def logout() -> dict:
        return apply_request_on_function(__system_service.logout)

    # 3.2
    @app.route(f'{API_BASE}/shops', methods=['POST'])
    def open_shop() -> dict:
        return apply_request_on_function(__system_service.open_shop)

    # 3.7
    @app.route(f'{API_BASE}/transactions')
    def get_personal_purchase_history() -> List[dict]:
        return jsonify(__system_service.get_personal_purchase_history(request.args.get("token")))

    # 4. Shop Owner Requirements

    # 4.1
    @app.route(f'{API_BASE}/shops/<int:shop_id>/products', methods=['POST'])
    def add_product_to_shop(shop_id: int) -> dict:
        return apply_request_on_function(
            __system_service.add_product_to_shop, shop_id=shop_id
        )

    # 4.1
    @app.route(f'{API_BASE}/shops/<int:shop_id>/products/<int:product_id>', methods=['PUT'])
    def edit_product_info(shop_id: int, product_id: int) -> dict:
        return apply_request_on_function(
            __system_service.edit_product_info,
            shop_id=shop_id, product_id=product_id
        )

    # 4.1
    @app.route(f'{API_BASE}/shops/<int:shop_id>/products/<int:product_id>', methods=['DELETE'])
    def delete_product(shop_id: int, product_id: int) -> dict:
        return apply_request_on_function(
            __system_service.delete_product,
            shop_id=shop_id, product_id=product_id
        )

    # 4.5
    # TODO: maybe add new manager username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/managers', methods=['POST'])
    def appoint_shop_manager(shop_id: int) -> dict:
        return apply_request_on_function(
            __system_service.appoint_shop_manager, shop_id=shop_id
        )

    # 4.3
    # TODO: maybe add new owner username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/owners', methods=['POST'])
    def appoint_shop_owner(shop_id: int) -> dict:
        return apply_request_on_function(__system_service.appoint_shop_owner, shop_id=shop_id)

    # 4.3
    # TODO: maybe add new owner username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/promotions', methods=['POST'])
    def promote_shop_owner(shop_id: int) -> dict:
        return apply_request_on_function(__system_service.promote_shop_owner, shop_id=shop_id)

    # 4.6
    # TODO: maybe add manager username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/managers', methods=['PUT'])
    def edit_manager_permissions(shop_id: int) -> dict:
        return apply_request_on_function(__system_service.edit_manager_permissions, shop_id=shop_id)

    # 4.7
    # TODO: maybe add manager username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/managers', methods=['DELETE'])
    def un_appoint_manager(shop_id: int) -> dict:
        return apply_request_on_function(__system_service.un_appoint_manager, shop_id=shop_id)

    # 4.7
    # TODO: maybe add owner username to url
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments/owners', methods=['DELETE'])
    def un_appoint_shop_owner(shop_id: int) -> dict:
        return apply_request_on_function(__system_service.un_appoint_shop_owner, shop_id=shop_id)

    # 4.9
    @app.route(f'{API_BASE}/shops/<int:shop_id>/appointments', methods=['GET'])
    def get_shop_staff_info(shop_id: int) -> List[dict]:
        return __system_service.get_shop_staff_info(request.args.get("token"), shop_id=shop_id)

    # 4.11
    @app.route(f'{API_BASE}/shops/<int:shop_id>/transactions', methods=['GET'])
    def get_shop_transaction_history(shop_id: int) -> List[dict]:
        return __system_service.get_shop_transaction_history(request.args.get("token"), shop_id=shop_id)

    # 6. System Administrator Requirements

    # 6.4
    @app.route(f'{API_BASE}/system/transactions')
    def get_system_transactions():
        return __system_service.get_system_transactions(request.args.get("token"))

    @app.route(f'{API_BASE}/system/transactions/shops/<int:shop_id>')
    def get_system_transactions_of_shop(shop_id):
        return __system_service.get_system_transactions_of_shop(request.args.get("token"), shop_id)

    # @app.route(f'{API_BASE}/system/transactions/shops')
    # def get_system_transactions_of_user(username):
    #     return apply_request_on_function(__system_service.get_system_transactions_of_user(username))

    @app.route(f'{API_BASE}/shops/<int:shop_id>/products/<int:product_id>')
    def get_product_info(shop_id: int, product_id: int):
        return __system_service.get_product_info(request.args.get("token"), shop_id, product_id)

    @app.route(f'{API_BASE}/permissions/<int:shop_id>')
    def get_permissions(shop_id: int):
        # print(__system_service.get_permissions(request.args.get("token"), shop_id))
        return __system_service.get_permissions(request.args.get("token"), shop_id)

    @app.route(f'{API_BASE}/shops/<int:shop_id>/discounts', methods=["GET"])
    def get_discounts(shop_id: int):
        ret = __system_service.get_discounts(token=request.args.get("token"), shop_id=shop_id)
        print(ret)
        return ret

    @app.route(f'{API_BASE}/shops/<int:shop_id>/discounts', methods=["POST"])
    def add_discount(shop_id: int):
        return apply_request_on_function(__system_service.add_discount, shop_id=shop_id)

    @app.route(f'{API_BASE}/shops/<int:shop_id>/discounts', methods=["DELETE"])
    def delete_discounts(shop_id: int):
        return apply_request_on_function(__system_service.delete_discounts, shop_id=shop_id)

    @app.route(f'{API_BASE}/shops/<int:shop_id>/discounts', methods=["PUT"])
    def aggregate_discounts(shop_id: int):
        return apply_request_on_function(__system_service.aggregate_discounts, shop_id=shop_id)

    @app.route(f'{API_BASE}/shops/<int:shop_id>/discounts/<int:dst_discount_id>', methods=["PUT"])
    def move_discount_to(shop_id: int, dst_discount_id: int):
        return apply_request_on_function(
            __system_service.move_discount_to, shop_id=shop_id, dst_discount_id=dst_discount_id
        )

    @app.route(f'{API_BASE}/appointments', methods=["GET"])
    def get_user_appointments():
        return __system_service.get_user_appointemnts(request.args.get("token"))

    @app.errorhandler(404)
    def server_error(e):
        return jsonify(error=str(e)), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True, ssl_context=('../secrets/cert.pem', '../secrets/key.pem'))
