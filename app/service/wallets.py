from fastapi import HTTPException
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest

def get_wallet(wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets()
        return {"total_balance": sum(wallets.values())}
    if wallets_repository.is_wallet_exists(wallet_name) is False:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    balance = wallets_repository.get_wallet_balance(wallet_name)
    
    return {"wallet": wallet_name, "balance": balance}

def create_wallet(request: CreateWalletRequest):
    if wallets_repository.is_wallet_exists(request.name):
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{request.name}' already exists"
        )

    new_balance = wallets_repository.create_wallet(request.name, request.initial_balance)
    return {
        "message": f"Wallet '{request.name}' created successfully",
        "wallet": request.name,
        "balance": new_balance
    }
