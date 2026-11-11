from fastapi import HTTPException

from app.repository.wallets import WalletRepository
from app.schemas import OperationRequest


class OperationService:
    def __init__(self, wallets: WalletRepository) -> None:
        self.wallets = wallets

    def add_income(self, operation: OperationRequest) -> dict[str, str | float | None]:
        wallet = self.wallets.get_wallet(operation.wallet_name)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found",
            )

        wallet = self.wallets.add_income(wallet, operation.amount)
        return {
            "message": "Income added successfully",
            "wallet_name": operation.wallet_name,
            "description": operation.description,
            "balance": wallet.balance,
        }

    def add_expense(self, operation: OperationRequest) -> dict[str, str | float | None]:
        wallet = self.wallets.get_wallet(operation.wallet_name)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found",
            )
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {wallet.balance}",
            )

        wallet = self.wallets.add_expense(wallet, operation.amount)
        return {
            "message": "Expense added successfully",
            "wallet_name": operation.wallet_name,
            "description": operation.description,
            "balance": wallet.balance,
        }
