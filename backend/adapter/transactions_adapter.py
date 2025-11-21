import json
import os

from fastapi import HTTPException, status
from sqlalchemy import Transaction
from sqlalchemy.orm import Session

from database import transactions as crud_transactions
from dotenv import load_dotenv

load_dotenv()

class TransactionAdapter:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.data_source = (os.getenv("DATA_SOURCE")).lower()
        self.json_path = "./database/transactions.json"

    def __fetch_json_data(self, user_id: int):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Arquivo JSON não encontrado: {self.json_path}",
            )

        user_transactions = [t for t in data if t.get("user_id") == user_id]

        return user_transactions

    def __fetch_db_data(self, user_id: int) -> list[Transaction]:
        if not self.db:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sessão de banco de dados não fornecida.",
            )

        return crud_transactions.get_transaction_by_user(self.db, user_id)

    def get_transactions(self, user_id: int) -> list[Transaction]:
        if self.data_source == "db":
            return self.__fetch_db_data(user_id)
        elif self.data_source == "json":
            return self.__fetch_json_data(user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fonte de dados inválida: {self.data_source}",
            )
