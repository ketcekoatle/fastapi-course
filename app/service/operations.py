from datetime import datetime
from fastapi import HTTPException
from app.enum import OperationTypeEnum
from app.repository.operations import OperationRepository
from app.repository.wallets import WalletRepository
from app.schemas import OperationRequest, OperationResponse


class OperationService:
    def __init__(self, wallets: WalletRepository, operations: OperationRepository) -> None:
        self.wallets = wallets
        self.operations = operations

    def add_income(self, operation: OperationRequest, user_id: int) -> OperationResponse:
        wallet = self.wallets.get_wallet(user_id, operation.wallet_name)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found",
            )

        wallet = self.wallets.add_income(wallet, operation.amount)
        operation = self.operations.create_operation(
            wallet_id=wallet.id,
            type=OperationTypeEnum.INCOME,
            amount=operation.amount,
            currency=wallet.currency,
        )
        return OperationResponse.model_validate(operation)

    def add_expense(self, operation: OperationRequest, user_id: int) -> OperationResponse:
        wallet = self.wallets.get_wallet(user_id, operation.wallet_name)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found",
            )
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {wallet.balance}",
            )

        wallet = self.wallets.add_expense(wallet, operation.amount)
        operation = self.operations.create_operation(
            wallet_id=wallet.id,
            type=OperationTypeEnum.EXPENSE,
            amount=operation.amount,
            currency=wallet.currency,
        )
        return OperationResponse.model_validate(operation)

    def get_operations(
        self,
        user_id: int,
        wallet_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[OperationResponse]:
        if wallet_id is not None:
            wallet = self.wallets.get_wallet_by_id(wallet_id, user_id)
            if wallet is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Wallet with ID '{wallet_id}' not found",
                )
            wallet_ids=[wallet_id]
            
        else:
            wallets = self.wallets.get_all_wallets(user_id)
            wallet_ids = [wallet.id for wallet in wallets]
        operations = self.operations.get_operations(
            wallet_ids=wallet_ids,
            date_from=date_from,
            date_to=date_to
        )
        return [OperationResponse.model_validate(op) for op in operations]

