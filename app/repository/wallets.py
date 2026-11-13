from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enum import CurrencyEnum
from app.enum import CurrencyEnum
from app.models import Wallet


class WalletRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_wallet(self, user_id: int, wallet_name: str) -> Wallet | None:
        stmt = select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
        return self.db.scalar(stmt)

    def get_all_wallets(self, user_id: int) -> list[Wallet]:
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        return self.db.scalars(stmt).all()

    def create_wallet(self, wallet_name: str, initial_balance: float, user_id: int,
                      currency: CurrencyEnum = CurrencyEnum.UAH) -> Wallet:
        wallet = Wallet(name=wallet_name, balance=initial_balance, user_id=user_id, currency=currency)
        self.db.add(wallet)
        self.db.flush()
        return wallet

    def add_income(self, wallet: Wallet, amount: float) -> Wallet:
        wallet.balance += amount
        return wallet

    def add_expense(self, wallet: Wallet, amount: float) -> Wallet:
        wallet.balance -= amount
        return wallet

    def get_wallet_by_id(self, wallet_id: int, user_id: int) -> Wallet | None:
        stmt = select(Wallet).where(Wallet.id == wallet_id, Wallet.user_id == user_id)
        return self.db.scalar(stmt)
