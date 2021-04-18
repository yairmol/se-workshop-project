from typing import List


class ICommerceSystemFacade:

    # Guest actions
    def enter(self) -> str:
        """enter the system. returns a session id for user identification"""
        raise NotImplementedError()

    def exit(self, user_id: int) -> bool:
        """exit the system"""
        raise NotImplementedError()

    def register(self, user_id: int, username: str, password: str, email: str, **additional_details) -> bool:
        """
        register a new user (subscriber) to the system
        :param user_id:
        :param username:
        :param password:
        :param email:
        :param additional_details: additional user details TBD
        :return: True on success
        """

    def login(self, user_id: int, username: str, password: str) -> bool:
        """
        associate the user identified by user_id with the profile of
        the subscribed user identified by username iff <username, password>
        is in the system
        :return: True on success - <username, password> is saved in the system
        """
        raise NotImplementedError()

    def logout(self, user_id: int) -> bool:
        """
        perform a logout to the user associated with the given user_id
        :param user_id:
        :return: True if the user identified by user_id was logged in
        """
        raise NotImplementedError()

    def get_shop_info(self, shop_id: int) -> dict:
        """
        returns a dictionary with shop information such as shop_name, products etc.
        """
        raise NotImplementedError()

    def save_product_to_cart(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int) -> bool:
        """
        saves a product to a shopping bag in the shopping cart of the user identified by user_id
        :param amount_to_buy: the amount of the product the user wants to save
        :param user_id: user identifier
        :param shop_id: the shop that sells the product
        :param product_id: the product being saved to cart
        :return: True if action was successful
        """
        raise NotImplementedError()

    def remove_product_from_cart(self, user_id: int, shop_id: int, product_id: int, amount: int):
        """
        removes a product from a shopping bag in the shopping cart of the user identified by user_id
        :param user_id: user identifier
        :param shop_id: the shop that sells the product
        :param product_id: the product being saved to cart
        :param amount: the amount of the product the user wants to remove
        :return: True if action was successful
        """
        raise NotImplementedError()

    def get_cart_info(self, user_id: int) -> dict:
        """
        returns a dictionary containing the cart information of the user identified by user_id
        in the format of

        {
            <shop_id>: {
                <shop_fields>
                products: [
                    <product-info-dictionary> for every product in the shop shopping bag
                ]
            } for every shop with a shopping bag in the user cart
        }

        """
        raise NotImplementedError()

    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        """
        search items in all shops using keywords and filters
        :param categories:
        :param product_name:
        :param keywords: a string containing the search keywords to be matched with products
        :param filters: a list of filters
        :return: a list of products (a product is represented by a dictionary)
        """
        raise NotImplementedError()

    def search_shops(self, keywords: str, filters: list) -> List[dict]:
        """
        search shops using keywords and filters
        :param keywords: a string containing the search keywords to be matched with shops
        :param filters: a list of filters
        :return: a list of products (a product is represented by a dictionary)
        """
        raise NotImplementedError()

    def purchase_cart(self, user_id: int, payment_details: dict, all_or_nothing: bool):
        """
        make a purchase of the entire shopping cart of a user (i.e. all shopping bags)
        :param all_or_nothing: true if the user wants all the cart or nothing at all
        :param payment_details: payment details of the user
        :param user_id: identifies the user making the purchase
        :return: true if the purchase was a success, false otherwise
        """
        raise NotImplementedError()

    def purchase_shopping_bag(self, user_id: int, shop_id: str, payment_details: dict):
        """
                make a purchase of the entire shopping bag for the specified store of a user
                :param shop_id: the shop that identifies the bag
                :param payment_details: payment details of the user
                :param user_id: identifies the user making the purchase
                :return: true if the purchase was a success, false otherwise
                """
        raise NotImplementedError()

    def purchase_product(self, user_id: int, shop_id: str, product_id: int, amount_to_buy: int, payment_details: dict):
        """
        buy a single product
        :param payment_details: payment details of the user
        :param amount_to_buy: amount of the product to buy
        :param user_id: session id of the user purchasing the product
        :param shop_id: the id of the shop in which the purchased product resides
        :param product_id: the id of the purchased product
        :return: True if action was successful
        """
        raise NotImplementedError()

    # Subscribed actions
    def open_shop(self, user_id: int, **shop_details) -> int:
        """
        opens a new shop in the system. the user identified by user_id is now the shop founder
        :return the shop id if operation was successful
        """
        raise NotImplementedError()

    def get_personal_purchase_history(self, user_id: int) -> List[dict]:
        """
        :param user_id: user identifier
        :return: returns a list of all transactions made by the user identified by user_id
        """
        raise NotImplementedError()

    # shop owner/manager actions
    def add_product_to_shop(self, user_id: int, shop_id: int, **product_info) -> int:
        """
        adds a new product to the shop identified by shop_id.
        this action succeeds iff the user identified by user_id has the proper authorization
        i.e. he is a shop owner or a shop manager with an 'add_product' permission.
        :return the product id if the operation was successful
        """
        raise NotImplementedError()

    def edit_product_info(
            self, user_id: int, shop_id: int, product_id: int,
            product_name: str, description: str, price: float, quantity: int
    ) -> bool:
        """
        edit the product info of a product identified by product_id in shop identified by shop_id.
        this action succeeds iff the user identified by user_id has the proper authorization
        i.e. he is a shop owner or a shop manager with an 'edit_product' permission.
        :return: True on success
        """
        raise NotImplementedError()

    def delete_product(self, user_id: int, shop_id: int, product_id: int) -> bool:
        """
        edit the product info of a product identified by product_id in shop identified by shop_id.
        this action succeeds iff the user identified by user_id has the proper authorization
        i.e. he is a shop owner or a shop manager with an 'delete_product' permission.
        """
        raise NotImplementedError()

    def appoint_shop_owner(self, user_id: int, shop_id: int, username: str) -> bool:
        """
        appoint the user identified by username as an owner of the shop identified by shop_id.
        this action succeeds iff the user identified by user_id has the proper authorization - he is a shop owner
        :param user_id: identifier for user performing the action
        :param shop_id: shop identifier
        :param username: username of the user to be appointed as shop owner
        :return: True on success
        """
        raise NotImplementedError()

    def promote_shop_owner(self, user_id: int, shop_id: int, username: str) -> bool:
        """
        promote a shop manager, to shop owner
        :param user_id: identifier for user performing the action
        :param shop_id: shop identifier
        :param username: username of the manager user to be appointed as shop owner
        :return: True on success
        """
        raise NotImplementedError()

    def appoint_shop_manager(self, user_id: int, shop_id: int, username: str, permissions: List[str]) -> bool:
        """
        appoint the user identified by username as a manager of the shop identified by shop_id with permissions
        given by permissions param.
        this action succeeds iff the user identified by user_id has the proper authorization - he is a shop owner
        :param user_id: identifier for user performing the action
        :param shop_id: shop identifier
        :param username: username of the user to be appointed as shop manager
        :param permissions: a list of permissions represented by strings for the newly appointed manager.
        possible values are ['add_product', 'edit_product', 'delete_product']
        :return: True on success
        """
        raise NotImplementedError()

    def edit_manager_permissions(self, user_id: int, shop_id: int, username: str, permissions: dict) -> bool:
        """
        this action succeeds iff the user identified by user_id has the proper authorization, the user identified
        bu username is a manager of the shop identified by shop_id and the permissions are legal
        :param user_id: identifier for user performing the action
        :param shop_id: shop identifier
        :param username: username of the user who is a shop manager
        :param permissions: a list of permissions represented by strings for the newly appointed manager.
        possible values are ['add_product', 'edit_product', 'delete_product']
        :return: True on success
        """
        raise NotImplementedError()

    def unappoint_shop_worker(self, user_id: int, shop_id: int, username: str) -> bool:
        """
        unappoint the user identified by username from his role in the shop identified by shop_id
        Action succeeds iff the user of session_id has authorization and user of username is a shop worker.
        """
        raise NotImplementedError()

    def unappoint_shop_manager(self, user_id: int, shop_id: str, username: str) -> bool:
        """
        unappoint, but for a specific role.
        """
        raise NotImplementedError()

    def unappoint_shop_owner(self, user_id: int, shop_id: str, username: str) -> bool:
        """
        unappoint, but for a specific role.
        """
        raise NotImplementedError()

    def get_shop_staff_info(self, shop_id: str) -> List[dict]:
        """
        Action succeeds iff user of user_id has proper authorization
        """
        raise NotImplementedError()

    def get_shop_transaction_history(self, user_id: int, shop_id: int) -> List[dict]:
        raise NotImplementedError()

    # system admin actions
    def get_system_transaction_history(self, user_id: int) -> List[dict]:
        raise NotImplementedError()
