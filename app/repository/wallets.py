from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Wallet

def is_wallet_exists(db: Session, wallet_name: str) -> bool:
    stmt = select(Wallet.id).where(Wallet.name == wallet_name)
    return db.scalar(stmt) is not None

def get_wallet(db: Session, wallet_name: str) -> Wallet:
    stmt = select(Wallet).where(Wallet.name == wallet_name)
    return db.scalars(stmt).one()

def add_income(db: Session, wallet_name: str, amount: float) -> Wallet:
    wallet = get_wallet(db, wallet_name)
    wallet.balance += amount
    return wallet

def add_expense(db: Session, wallet_name: str, amount: float) -> Wallet:
    wallet = get_wallet(db, wallet_name)
    wallet.balance -= amount
    return wallet

def get_all_wallets(db: Session) -> list[Wallet]:
    stmt = select(Wallet)
    return db.execute(stmt).scalars().all()

def create_wallet(db: Session, wallet_name: str, initial_balance: float) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=initial_balance)
    db.add(wallet)
    return wallet
