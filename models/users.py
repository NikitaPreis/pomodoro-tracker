from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(nullable=False, unique=True)
    access_token: Mapped[str] = mapped_column(nullable=False, unique=True)
