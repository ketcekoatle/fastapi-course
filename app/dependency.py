from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import UserResponse
from app.repository.users import UserRepository
from app.repository.wallets import WalletRepository
from app.service.operations import OperationService
from app.service.users import UserService
from app.service.wallets import WalletService

security = HTTPBearer()


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


def get_user_service(
    db: Session = Depends(get_db, scope="function"),
) -> UserService:
    return UserService(UserRepository(db))


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    login = credentials.credentials
    try:
        return user_service.get_user(login)
    except HTTPException as exc:
        if exc.status_code != 404:
            raise
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
