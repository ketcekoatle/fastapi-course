from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enum import CurrencyEnum, OperationTypeEnum
from app.models import Operation


class OperationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_operation(
        self, 
        wallet_id: int,
        type: OperationTypeEnum,
        amount: float,
        currency: CurrencyEnum,
        category: str | None = None,
        subcategory: str | None = None
    ) -> Operation:
        operation = Operation(
            wallet_id=wallet_id,
            type=type,
            amount=amount,
            currency=currency,
            category=category,
            subcategory=subcategory,
        )
        self.db.add(operation)
        self.db.flush()
        return operation

    def get_operations(
        self,
        wallet_ids: list[int] = [],
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Operation]:
        stmt = select(Operation).where(Operation.wallet_id.in_(wallet_ids))

        if date_from is not None:
            stmt = stmt.where(Operation.created_at >= date_from.isoformat())
        if date_to is not None:
            stmt = stmt.where(Operation.created_at <= date_to.isoformat())

        return list(self.db.scalars(stmt).all())
