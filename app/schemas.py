from pydantic import BaseModel, Field, field_validator


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(default=None, max_length=255)

    @field_validator("amount")
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be a positive number")
        return v

    @field_validator("wallet_name")
    def wallet_name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Wallet name must not be empty")
        return v

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator("initial_balance")
    def initial_balance_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Initial balance must be a non-negative number")
        return v

    @field_validator("name")
    def wallet_name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Wallet name must not be empty")
        return v