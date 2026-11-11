from fastapi import APIRouter, Depends

from app.dependency import get_current_user, get_operation_service
from app.schemas import OperationRequest, UserResponse
from app.service.operations import OperationService

router = APIRouter(dependencies=[Depends(get_current_user)],)

@router.post("/operations/income")
def add_income(
    operation: OperationRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: OperationService = Depends(get_operation_service),
):
    return service.add_income(operation, current_user.id)

@router.post("/operations/expense")
def add_expense(
    operation: OperationRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: OperationService = Depends(get_operation_service),
):
    return service.add_expense(operation, current_user.id)
