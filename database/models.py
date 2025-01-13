from typing import Any, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]
