from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_settings.models import UserSettings
from app.users.user_settings.schema import UserSettingsUpdateSchema


class UserSettingsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_settings_by_user_id(
        self, user_id: int
    ) -> UserSettings:
        query = select(UserSettings).where(UserSettings.user_id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user_settings(self, user_id: int) -> int:
        stmt = insert(UserSettings).values(user_id=user_id).returning(UserSettings.id)
        async with self.db_session as session:
            user_settings_id = (await session.execute(
                stmt
            )).scalar_one()
            await session.commit()
        return user_settings_id

    async def update_pomodoro_duration(
        self, user_id: int, pomodoro_duration: int
    ) -> UserSettings:
        """Update value of pomodoro duration in db."""

        stmt = update(UserSettings).where(
            UserSettings.user_id == user_id
        ).values(
            pomodoro_duration=pomodoro_duration
        )
        async with self.db_session as session:
            await session.execute(stmt)
            await session.commit()
            return await self.get_user_settings_by_user_id(user_id=user_id)

    async def update_short_break_duration(
        self, user_id: int, short_break_duration: int
    ) -> UserSettings:
        """Update value of short break duration between pomodoros."""

        stmt = update(UserSettings).where(
            UserSettings.user_id == user_id
        ).values(
            short_break_duration=short_break_duration
        )
        async with self.db_session as session:
            await session.execute(stmt)
            await session.commit()
            return await self.get_user_settings_by_user_id(user_id=user_id)

    async def update_long_break_duration(
        self, user_id: int, long_break_duration: int
    ) -> UserSettings:
        """Update value of short break duration between pomodoros."""

        stmt = update(UserSettings).where(
            UserSettings.user_id == user_id
        ).values(
            long_break_duration=long_break_duration
        )
        async with self.db_session as session:
            await session.execute(stmt)
            await session.commit()
            return await self.get_user_settings_by_user_id(user_id=user_id)

    async def update_long_break_interval(
        self, user_id: int, long_break_interval: int
    ) -> UserSettings:
        """Update value of interval between long break duration between pomodoros."""

        stmt = update(UserSettings).where(
            UserSettings.user_id == user_id
        ).values(
            long_break_interval=long_break_interval
        )
        async with self.db_session as session:
            await session.execute(stmt)
            await session.commit()
            return await self.get_user_settings_by_user_id(user_id=user_id)

    async def reset_settings(
        self, user_id: int, user_settings: UserSettingsUpdateSchema
    ) -> UserSettings:
        """Reset user settings to default."""
        stmt = update(UserSettings).where(
            UserSettings.user_id == user_id
        ).values(**user_settings.model_dump())
        async with self.db_session as session:
            await session.execute(stmt)
            await session.commit()
            return await self.get_user_settings_by_user_id(user_id=user_id)
