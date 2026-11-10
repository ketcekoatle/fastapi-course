from fastapi import HTTPException
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest
from app.database import SessionLocal

def get_wallet(wallet_name: str | None = None) -> dict[str, float]:
    with SessionLocal.begin() as db:
        if wallet_name is None:
            wallets = wallets_repository.get_all_wallets(db)
            return {"total_balance": sum(wallet.balance for wallet in wallets)}
        if wallets_repository.is_wallet_exists(db, wallet_name) is False:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_name}' not found"
            )
        wallet = wallets_repository.get_wallet(db, wallet_name)
    return {"wallet": wallet.name, "balance": wallet.balance}

def create_wallet(request: CreateWalletRequest):
    with SessionLocal.begin() as db:
        if wallets_repository.is_wallet_exists(db, request.name) is True:
            raise HTTPException(
                status_code=400,
                detail=f"Wallet '{request.name}' already exists"
            )

        wallet = wallets_repository.create_wallet(db, request.name, request.initial_balance)
    return {
        "message": f"Wallet '{request.name}' created successfully",
        "wallet": request.name,
        "balance": wallet.balance
    }
