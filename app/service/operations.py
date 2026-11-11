from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository import wallets as wallets_repository
from app.schemas import OperationRequest

def add_income(db: Session, operation: OperationRequest):
    if wallets_repository.is_wallet_exists(db, operation.wallet_name) is False:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)
   
    return {
        "message": "Income added successfully",
        "wallet_name": operation.wallet_name,
        "description": operation.description,
        "balance": wallet.balance
    }

def add_expense(db: Session, operation: OperationRequest):
    if wallets_repository.is_wallet_exists(db, operation.wallet_name) is False:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    wallet = wallets_repository.get_wallet(db, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.balance}"
        )
    wallet = wallets_repository.add_expense(db, operation.wallet_name, operation.amount)
    
    return {
        "message": "Expense added successfully",
        "wallet_name": operation.wallet_name,
        "description": operation.description,
        "balance": wallet.balance
    }

