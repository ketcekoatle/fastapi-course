from fastapi import HTTPException

from app.repository.wallets import WalletRepository
from app.schemas import CreateWalletRequest


class WalletService:
    def __init__(self, wallets: WalletRepository) -> None:
        self.wallets = wallets

    def get_wallet(self, wallet_name: str | None = None) -> dict[str, str | float]:
        if wallet_name is None:
            wallets = self.wallets.get_all_wallets()
            return {"total_balance": sum(wallet.balance for wallet in wallets)}

        wallet = self.wallets.get_wallet(wallet_name)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_name}' not found",
            )

        return {"wallet": wallet.name, "balance": wallet.balance}

    def create_wallet(self, request: CreateWalletRequest) -> dict[str, str | float]:
        if self.wallets.get_wallet(request.name) is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Wallet '{request.name}' already exists",
            )

        wallet = self.wallets.create_wallet(request.name, request.initial_balance)
        return {
            "message": f"Wallet '{request.name}' created successfully",
            "wallet": wallet.name,
            "balance": wallet.balance,
        }
