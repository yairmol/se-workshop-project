from typing import List

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
        self._transactions.append(transaction)

    def get_transactions(self):
        return self._transactions

    def cleanup(self):
        self._transactions.clear()
