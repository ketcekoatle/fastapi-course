from fastapi import APIRouter, Depends

from app.dependency import get_operation_service
from app.schemas import OperationRequest
from app.service.operations import OperationService

router = APIRouter()

@router.post("/operations/income")
def add_income(
    operation: OperationRequest,
    service: OperationService = Depends(get_operation_service),
):
    return service.add_income(operation)

@router.post("/operations/expense")
def add_expense(
    operation: OperationRequest,
    service: OperationService = Depends(get_operation_service),
):
    return service.add_expense(operation)
