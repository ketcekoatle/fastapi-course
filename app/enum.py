from enum import StrEnum, auto

class CurrencyEnum(StrEnum):
     USD = "USD"
     EUR = "EUR"
     UAH = "UAH"

class OperationTypeEnum(StrEnum):
    INCOME = auto()
    EXPENSE = auto()