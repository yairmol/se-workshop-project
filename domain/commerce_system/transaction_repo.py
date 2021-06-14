from typing import List

from data_access_layer.engine import save, add_to_session, delete_all
from domain.commerce_system.transaction import Transaction


class TransactionRepo:
    __INSTANCE = None

    @staticmethod
    def get_transaction_repo():
        if not TransactionRepo.__INSTANCE:
            TransactionRepo.__INSTANCE = TransactionRepo()
        return TransactionRepo.__INSTANCE

    def __init__(self):
        self._transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        # save(Transaction, transaction)
        self._transactions.append(transaction)

    # @add_to_session
    def get_transactions(self):
        return self._transactions

    # @add_to_session
    def get_transactions_of_shop(self, shop_id):
        return filter(lambda trans: trans.id == shop_id, self._transactions)

    # @add_to_session
    def get_transactions_of_user(self, username):
        return filter(lambda trans: trans.username == username, self._transactions)

    def cleanup(self):
        # delete_all(Transaction)
        self._transactions.clear()

    # def get_transactions_by_id(self):
