from ..database.models import Transaction
from ..dto.transactions_dto import TransactionRegisterResponse, TransactionsListResponse


class TransactionAdapter:
    @staticmethod
    def to_response(transaction: Transaction) -> TransactionRegisterResponse:
        return TransactionRegisterResponse(
            transaction_id=transaction.transaction_id,
            transaction_date=transaction.transaction_date,
            transaction_value=transaction.transaction_value,
            transaction_type=transaction.transaction_type,
            transaction_category=transaction.transaction_category,
            transaction_description=transaction.transaction_description,
        )

    @staticmethod
    def to_list_response(
        transactions: list[Transaction],
    ) -> list[TransactionsListResponse]:
        return [
            TransactionsListResponse(
                transaction_id=t.transaction_id,
                transaction_date=t.transaction_date,
                transaction_value=t.transaction_value,
                transaction_type=t.transaction_type,
                transaction_category=t.transaction_category,
                transaction_description=t.transaction_description,
            )
            for t in transactions
        ]
