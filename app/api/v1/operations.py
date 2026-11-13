from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.dependency import get_current_user, get_operation_service
from app.schemas import OperationRequest, OperationResponse, UserResponse
from app.service.operations import OperationService

router = APIRouter(dependencies=[Depends(get_current_user)],)

@router.post("/operations/income", response_model=OperationResponse)
def add_income(
    operation: OperationRequest,
    user: UserResponse = Depends(get_current_user),
    service: OperationService = Depends(get_operation_service),
):
    return service.add_income(operation, user.id)

@router.post("/operations/expense", response_model=OperationResponse)
def add_expense(
    operation: OperationRequest,
    user: UserResponse = Depends(get_current_user),
    service: OperationService = Depends(get_operation_service),
):
    return service.add_expense(operation, user.id)

@router.get("/operations", response_model=list[OperationResponse])
def get_operations(
    wallet_id: int | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    user: UserResponse = Depends(get_current_user),
    service: OperationService = Depends(get_operation_service),
):
    return service.get_operations(user.id, wallet_id, date_from, date_to)