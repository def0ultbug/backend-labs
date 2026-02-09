from enum import Enum

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

class Base(DeclarativeBase):
    pass

class Role(str,Enum):
    BASIC = "basic"
    PREMIUM = "premium"

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )

    username : Mapped[str] = mapped_column(
        unique=True, index=True
    )

    email : Mapped[str] = mapped_column(
        unique=True, index=True
    )

    hash_password : Mapped[str] = mapped_column()

    role : Mapped[Role] = mapped_column(
        default=Role.BASIC
    )
    
    # for the MFA feature
    mfa_secret: Mapped[str] = mapped_column(
        nullable=True
    )
