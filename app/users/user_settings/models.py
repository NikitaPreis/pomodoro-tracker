from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import (DEFAULT_POMODORO_DURATION,
                           DEFAULT_SHORT_BREAK_DURATION,
                           DEFAULT_LONG_BREAK_DURATION,
                           DEFAULT_LONG_BREAK_INTERVAL)
from app.infrastructure.database import Base


class UserSettings(Base):
    """User settings for customising work with pomodoros.
    """
    __tablename__ = 'user_settings'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )

    # Duration of pomodoro (Type: integer; Refers to minutes).
    pomodoro_duration: Mapped[int] = mapped_column(
        default=DEFAULT_POMODORO_DURATION
    )

    # Duration of short break between pomodoros
    # (Type: integer; Refers to minutes).
    short_break_duration: Mapped[int] = mapped_column(
        default=DEFAULT_SHORT_BREAK_DURATION
    )

    # Duration of long break between pomodoros
    # (Type: integer; Refers to minutes).
    long_break_duration: Mapped[int] = mapped_column(
        default=DEFAULT_LONG_BREAK_DURATION
    )

    # Amount of pomodoros between long breaks.
    # (Type: integer; Refers to pomodoros amount).
    long_break_interval: Mapped[int] = mapped_column(
        default=DEFAULT_LONG_BREAK_INTERVAL
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_profiles.id'), nullable=False
    )
