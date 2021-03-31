from typing import List


class ICommerceSystemFacade:

    def enter(self) -> str:
        """enter the system. returns a session id for user identification"""
        raise NotImplementedError()

    def exit(self, session_id: str) -> bool:
        """exit the system"""
        raise NotImplementedError()

    def register(self, session_id: str, username: str, password: str, email: str, **kwargs) -> bool:
        raise NotImplementedError()

    def login(self, session_id: str, username: str, password: str) -> bool:
        raise NotImplementedError()

    def logout(self, session_id: str) -> bool:
        raise NotImplementedError()

    def get_shop_info(self, shop_id: str) -> dict:
        """
        :return: a dictionary with the shop information
        """
        raise NotImplementedError()

    def save_product_to_cart(self, session_id: str, shop_id: str, product_id: str) -> bool:
        """
        saves a product to a shopping bag in the shopping cart of the user ide
        :param session_id: user identifier
        :param shop_id: the shop that sells the product
        :param product_id: the product being saved to cart
        :return: True if action was successful
        """
        raise NotImplementedError()

    def get_cart_info(self, session_id: str) -> dict:
        """
        :param session_id: user identifier
        :return: a dictionary containing the cart information of the user identified by session_id
        """
        raise NotImplementedError()

    def search_products(self, keywords: str, filters: list) -> List[dict]:
        """
        search items in all shops using keywords and filters
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

    def purchase_cart(self, session_id: str) -> bool:
        """
        make a purchase of the entire shopping cart of a user (i.e. all shopping bags)
        :param session_id: identifies the user making the purchase
        :return: True if the action succeeded
        """
        raise NotImplementedError()

    def purchase_product(self, session_id: str, shop_id: str, product_id: str) -> bool:
        """
        buy a single product
        :param session_id: session id of the user purchasing the product
        :param shop_id: the id of the shop in which the purchased product resides
        :param product_id: the id of the purchased product
        :return: True if action was successful
        """
        raise NotImplementedError()

    def open_shop(self, session_id: str, **shop_details) -> bool:
        """
        opens a new shop in the system. the user identified by session_id is now the shop founder
        """
        raise NotImplementedError()

    def get_personal_purchase_history(self, session_id: str) -> List[dict]:
        """
        :param session_id: user identifier
        :return: returns a list of all transactions made by the user identified by session_id
        """
        raise NotImplementedError()

    def add_product_to_shop(self, session_id: str, shop_id: str, **product_info) -> bool:
        """
        adds a new product to the shop identified by shop_id.
        check for user permissions with session_id
        """
        raise NotImplementedError()

    def edit_product_info(self, session_id: str, shop_id: str, **product_info) -> bool:
        raise NotImplementedError()

    def delete_product(self, session_id: str, shop_id: str, product_id: str) -> bool:
        raise NotImplementedError()

    def appoint_shop_owner(self, session_id: str, shop_id: str, username: str) -> bool:
        raise NotImplementedError()

    def appoint_shop_manager(self, session_id: str, shop_id: str, username: str, permissions: dict) -> bool:
        raise NotImplementedError()

    def edit_manager_permissions(self, session_id: str, shop_id: str, username: str, permissions: dict) -> bool:
        raise NotImplementedError()

    def unappoint_shop_worker(self, session_id: str, shop_id: str, username: str) -> bool:
        raise NotImplementedError()

    def get_shop_staff_info(self, session_id: str, shop_id: str) -> List[dict]:
        raise NotImplementedError()

    def get_shop_transaction_history(self, session_id: str, shop_id: str) -> List[dict]:
        raise NotImplementedError()

    def get_system_transaction_history(self, session_id: str) -> List[dict]:
        raise NotImplementedError()
