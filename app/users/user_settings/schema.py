from pydantic import BaseModel

from app.constants import (DEFAULT_LONG_BREAK_DURATION,
                           DEFAULT_LONG_BREAK_INTERVAL,
                           DEFAULT_POMODORO_DURATION,
                           DEFAULT_SHORT_BREAK_DURATION)


class UserSettingsSchema(BaseModel):
    pomodoro_duration: int
    short_break_duration: int
    long_break_duration: int
    long_break_interval: int
    user_id: int

    class Config:
        from_attributes = True


class UserSettingsUpdateSchema(BaseModel):
    pomodoro_duration: int = DEFAULT_POMODORO_DURATION
    short_break_duration: int = DEFAULT_SHORT_BREAK_DURATION
    long_break_duration: int = DEFAULT_LONG_BREAK_DURATION
    long_break_interval: int = DEFAULT_LONG_BREAK_INTERVAL

    class Config:
        from_attributes = True
