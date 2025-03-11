from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('user_profiles.id'), nullable=False
    )

    __table_args__ = (UniqueConstraint(
        'name', 'user_id', name='_category_name_user'),
    )
