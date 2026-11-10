from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    balance: Mapped[float] = mapped_column(default=0.0)