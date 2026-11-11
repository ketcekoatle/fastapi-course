
from fastapi import HTTPException

from app.repository.users import UserRepository
from app.schemas import UserRequest, UserResponse


class UserService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def get_user(self, login: str) -> UserResponse:
        user = self.users.get_user(login)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User '{login}' not found",
            )
        return UserResponse.model_validate(user)

    def create_user(self, payload: UserRequest) -> UserResponse:
        if self.users.get_user(payload.login) is not None:
            raise HTTPException(
                status_code=400,
                detail=f"User '{payload.login}' already exists",
            )
        user = self.users.create_user(payload.login, payload.email, "temporary_password")
        # user = self.users.create_user(payload.login, payload.email, payload.password)
        return UserResponse.model_validate(user)
