from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Wallet


class WalletRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_wallet(self, wallet_name: str) -> Wallet | None:
        stmt = select(Wallet).where(Wallet.name == wallet_name)
        return self.db.scalar(stmt)

    def get_all_wallets(self) -> list[Wallet]:
        stmt = select(Wallet)
        return self.db.scalars(stmt).all()

    def create_wallet(self, wallet_name: str, initial_balance: float) -> Wallet:
        wallet = Wallet(name=wallet_name, balance=initial_balance)
        self.db.add(wallet)
        return wallet

    def add_income(self, wallet: Wallet, amount: float) -> Wallet:
        wallet.balance += amount
        return wallet

    def add_expense(self, wallet: Wallet, amount: float) -> Wallet:
        wallet.balance -= amount
        return wallet
