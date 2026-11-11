from fastapi import APIRouter, Depends

from app.dependency import get_wallet_service
from app.schemas import CreateWalletRequest
from app.service.wallets import WalletService

router = APIRouter()

@router.get("/balance")
def get_balance(
    wallet_name: str | None = None,
    service: WalletService = Depends(get_wallet_service),
):
    return service.get_wallet(wallet_name)

@router.post("/wallets")
def create_wallet(
    request: CreateWalletRequest,
    service: WalletService = Depends(get_wallet_service),
):
    return service.create_wallet(request)
