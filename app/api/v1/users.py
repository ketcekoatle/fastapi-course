from fastapi import APIRouter, Depends

from app.dependency import get_user_service
from app.dependency import get_current_user as dependencies_get_current_user
from app.schemas import UserRequest
from app.service.users import UserService
from app.service.users import UserResponse

router = APIRouter(dependencies=[Depends(dependencies_get_current_user)],)

@router.post(path="/users", response_model=UserResponse)
def create_user(
    payload: UserRequest,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(payload)

@router.get(path="/users/me", response_model=UserResponse)
def get_current_user(
    current_user: UserResponse = Depends(dependencies_get_current_user)
):
    return current_user