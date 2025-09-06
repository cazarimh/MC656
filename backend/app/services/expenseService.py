import json
import logging
import os
from datetime import datetime

from app.models.expenseModel import Expense
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ExpenseService:
    def __init__(self) -> None:
        expenses_path = os.getenv("EXPENSES_DATA_PATH")

        if not expenses_path:
            raise ValueError("EXPENSES_DATA_PATH not found in environment variables")

        self.data_file_path: str = expenses_path

        if not os.path.exists(self.data_file_path):
            logger.error(f"File does not exist at path: {self.data_file_path}")
            raise FileNotFoundError(
                f"Expenses data file not found at {self.data_file_path}"
            )

    async def _load_expenses_data(self) -> list[Expense]:
        """
        Load data from json file
        """
        logger.info(f"Loading expenses data from {self.data_file_path}")

        try:
            with open(self.data_file_path, "r") as file:
                logger.info("Fetching data from json file")
                raw_expenses = json.load(file)

                expenses = []
                for expense_data in raw_expenses:
                    expense_dict = expense_data.copy()

                    date_str = expense_dict.get("date")
                    if isinstance(date_str, str):
                        try:
                            expense_dict["date"] = datetime.fromisoformat(date_str)
                        except ValueError as e:
                            logger.error(f"Failed to parse date '{date_str}': {e}")
                            continue

                    try:
                        expense = Expense(**expense_dict)
                        expenses.append(expense)
                    except Exception as e:
                        logger.error(
                            f"Error creating expense model from {expense_dict}: {e}"
                        )
                        continue

                return expenses

        except Exception as e:
            logger.error(f"Failed to load data from json file: {e}")
            raise e

    async def getExpenseByUserId(self, userId: int) -> list[Expense]:
        logger.info(f"Fetching expenses for user ID: {userId}")
        expenseData = await self._load_expenses_data()

        userExpenses = [expense for expense in expenseData if expense.user_id == userId]
        logger.info(f"Found {len(userExpenses)} expenses for user ID: {userId}")

        return userExpenses

