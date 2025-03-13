from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column(
        nullable=True, unique=True
    )
    password: Mapped[str] = mapped_column(nullable=True, unique=True)
    google_access_token: Mapped[Optional[str]]
    yandex_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    user_settings = relationship(
        'UserSettings', backref='user_data', uselist=False
    )
