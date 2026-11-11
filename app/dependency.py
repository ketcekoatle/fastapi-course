from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repository.wallets import WalletRepository
from app.service.operations import OperationService
from app.service.wallets import WalletService


def get_db() -> Generator[Session, None, None]:
    with SessionLocal.begin() as db:
        yield db


def get_wallet_service(
    db: Session = Depends(get_db, scope="function"),
) -> WalletService:
    return WalletService(WalletRepository(db))


def get_operation_service(
    db: Session = Depends(get_db, scope="function"),
) -> OperationService:
    return OperationService(WalletRepository(db))
