from fastapi import APIRouter, Depends

from app.dependency import get_current_user, get_wallet_service
from app.schemas import CreateWalletRequest, UserResponse
from app.service.wallets import WalletService

router = APIRouter(dependencies=[Depends(get_current_user)],)

@router.get("/balance")
def get_balance(
    wallet_name: str | None = None,
    current_user: UserResponse = Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return service.get_wallet(current_user.id, wallet_name)

@router.post("/wallets")
def create_wallet(
    request: CreateWalletRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return service.create_wallet(request, current_user.id)
