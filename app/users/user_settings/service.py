from dataclasses import dataclass

from app.exception import (UserSettingsNotFoundException,
                           UserSettingsCreatingException)
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_settings.models import UserSettings
from app.users.user_settings.schema import (UserSettingsSchema,
                                            UserSettingsUpdateSchema)
from app.users.user_settings.repository import UserSettingsRepository


@dataclass
class UserSettingsService:
    user_settings_repository: UserSettingsRepository

    async def get_user_settings(self, user_id: int) -> UserSettingsSchema:
        """Get UserSettings obj from db by user_id."""
        user_settings: UserSettings = await self._get_user_settings_or_404(
            user_id=user_id
        )
        return UserSettingsSchema.model_validate(user_settings)

    async def create_user_settings(self, user_id: int) -> int:
        """Create UserSettings obj in db."""
        try:
            user_settings_id: int = (await
                self.user_settings_repository.create_user_settings(
                    user_id=user_id
                )
            )
        except Exception as _:
            raise UserSettingsCreatingException
        return user_settings_id

    async def set_pomodoro_duration(
        self, user_id: int, pomodoro_duration: int
    ):
        """Set duration of pomodoros in minutes (int)."""

        await self._check_user_settings_exists(user_id=user_id)
        updated_user_settings: UserSettings = (await
            self.user_settings_repository.update_pomodoro_duration(
                user_id=user_id, pomodoro_duration=pomodoro_duration
            )
        )
        return UserSettingsSchema.model_validate(updated_user_settings)

    async def set_pomodoro_short_break_duration(
        self, user_id: int, short_break_duration: int
    ):
        """Set duration of short breaks between pomodoros in minutes."""

        await self._check_user_settings_exists(user_id=user_id)
        updated_user_settings: UserSettings = (await
            self.user_settings_repository.update_short_break_duration(
                user_id=user_id, short_break_duration=short_break_duration
            )
        )
        return UserSettingsSchema.model_validate(updated_user_settings)

    async def set_pomodoro_long_break_duration(
        self, user_id: int, long_break_duration: int
    ):
        """Set duration of long breaks between pomodoros in minutes."""

        await self._check_user_settings_exists(user_id=user_id)
        updated_user_settings: UserSettings = (await
            self.user_settings_repository.update_long_break_duration(
                user_id=user_id, long_break_duration=long_break_duration
            )
        )
        return UserSettingsSchema.model_validate(updated_user_settings)

    async def set_interval_between_long_breaks(
        self, user_id: int, long_break_interval: int
    ):
        """Set interval between long breaks.

        Args:
            1) user_id (user id from request);
            2) long_break_intervals
               (How many pomodoros are between long breaks).
        """

        await self._check_user_settings_exists(user_id=user_id)
        updated_user_settings: UserSettings = (await
            self.user_settings_repository.update_long_break_interval(
                user_id=user_id, long_break_interval=long_break_interval
            )
        )
        return UserSettingsSchema.model_validate(updated_user_settings)

    async def reset_settings(self, user_id: int) -> UserSettingsSchema:
        """Reset user settings to default."""
    
        await self._check_user_settings_exists(user_id=user_id)

        # Create user settings update schema with default values.
        default_user_update_schema = UserSettingsUpdateSchema()

        updated_user_settings = (await
            self.user_settings_repository.reset_settings(
                user_id=user_id, user_settings=default_user_update_schema
            )
        )
        return UserSettingsSchema.model_validate(updated_user_settings)

    async def _get_user_settings_or_404(self, user_id: int) -> UserSettings:
        """Get user settings from db or get error 404."""
        user_settings = (await
            self.user_settings_repository.get_user_settings_by_user_id(
                user_id=user_id
            )
        )
        if not user_settings:
            raise UserSettingsNotFoundException
        return user_settings

    async def _check_user_settings_exists(self, user_id: int) -> UserSettings:
        """Check that user settings obj exists or get error 404."""
        return await self._get_user_settings_or_404(user_id=user_id)
