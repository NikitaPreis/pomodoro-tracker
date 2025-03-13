import enum

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class TaskStatusEnum(str, enum.Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    status: Mapped[TaskStatusEnum] = mapped_column(
        default=TaskStatusEnum.PENDING,
        server_default=text("'PENDING'")
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey('user_profiles.id'), nullable=False
    )
