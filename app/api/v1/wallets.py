from fastapi import APIRouter, Depends

from app.dependency import get_current_user, get_wallet_service
from app.schemas import CreateWalletRequest, TotalBalanceResponse, UserResponse, WalletResponse
from app.service.wallets import WalletService

router = APIRouter(dependencies=[Depends(get_current_user)],)

@router.get("/balance", response_model=WalletResponse | TotalBalanceResponse)
def get_balance(
    wallet_name: str | None = None,
    user: UserResponse = Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return service.get_wallet(user.id, wallet_name)

@router.post("/wallets", response_model=WalletResponse)
def create_wallet(
    request: CreateWalletRequest,
    user: UserResponse = Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return service.create_wallet(request, user.id)
