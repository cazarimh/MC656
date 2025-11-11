from database.models import Transaction
from dto.transactions_dto import TransactionRegisterResponse, TransactionsListResponse


class TransactionMapper:
    @staticmethod
    def to_response(transaction) -> TransactionRegisterResponse:
        """
        Converte um registro único (Transaction ou dict) em um DTO de resposta.
        """
        if isinstance(transaction, dict):
            # Quando vem do JSON
            return TransactionRegisterResponse(
                transaction_id=transaction.get("transaction_id"),
                transaction_date=transaction.get("transaction_date"),
                transaction_value=transaction.get("transaction_value"),
                transaction_type=transaction.get("transaction_type"),
                transaction_category=transaction.get("transaction_category"),
                transaction_description=transaction.get("transaction_description"),
            )
        elif isinstance(transaction, Transaction):
            # Quando vem do banco
            return TransactionRegisterResponse(
                transaction_id=transaction.transaction_id,
                transaction_date=transaction.transaction_date,
                transaction_value=transaction.transaction_value,
                transaction_type=transaction.transaction_type,
                transaction_category=transaction.transaction_category,
                transaction_description=transaction.transaction_description,
            )
        else:
            raise TypeError(
                f"Tipo inesperado ao mapear transação: {type(transaction).__name__}"
            )

    @staticmethod
    def to_list_response(transactions: list) -> list[TransactionsListResponse]:
        """
        Converte uma lista de transações (Transaction ou dict) em DTOs.
        """
        mapped = []
        for t in transactions:
            if isinstance(t, dict):
                mapped.append(
                    TransactionsListResponse(
                        transaction_id=t.get("transaction_id"),
                        transaction_date=t.get("transaction_date"),
                        transaction_value=t.get("transaction_value"),
                        transaction_type=t.get("transaction_type"),
                        transaction_category=t.get("transaction_category"),
                        transaction_description=t.get("transaction_description"),
                    )
                )
            elif isinstance(t, Transaction):
                mapped.append(
                    TransactionsListResponse(
                        transaction_id=t.transaction_id,
                        transaction_date=t.transaction_date,
                        transaction_value=t.transaction_value,
                        transaction_type=t.transaction_type,
                        transaction_category=t.transaction_category,
                        transaction_description=t.transaction_description,
                    )
                )
            else:
                raise TypeError(
                    f"Tipo inesperado na lista de transações: {type(t).__name__}"
                )
        return mapped
