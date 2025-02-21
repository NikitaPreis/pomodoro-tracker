import pytest
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.auth.service import AuthService
from app.users.user_profile.models import UserProfile
from tests.fixtures.users.user_model import (EXISTS_GOOGLE_USER_ID,
                                             EXISTS_GOOGLE_USER_EMAIL)


class TestAuthService:

    async def test_google_auth__login_not_exist_user(
            self, auth_service: AuthService,
            get_db_session: AsyncSession
        ):
            session = get_db_session
            code = 'fake_code'

            async with session as session:
                users = (await session.execute(
                    select(UserProfile)
                )).scalars().all()
            user = await auth_service.google_auth(code=code)

            assert len(users) == 0
            assert user is not None

            async with session as session:
                login_user = (await session.execute(
                    select(UserProfile).where(UserProfile.id == user.user_id)
                )).scalars().first()
            
            assert login_user is not None

    async def test_google_auth__login_exist_user(
        self, auth_service: AuthService, get_db_session: AsyncSession
    ):
        session = get_db_session
        query_create_user = insert(UserProfile).values(
            id=EXISTS_GOOGLE_USER_ID,
            email=EXISTS_GOOGLE_USER_EMAIL
        )
        query_get_user = select(UserProfile)

        code = 'fake_code'

        async with session as session:
            await session.execute(query_create_user)
            await session.commit()
            user_data = await auth_service.google_auth(code=code)

        async with session as session:
            login_user = (await session.execute(
                query_get_user.where(UserProfile.id == user_data.user_id)
            )).scalar_one_or_none()

        assert login_user.email == EXISTS_GOOGLE_USER_EMAIL
        assert user_data.user_id == EXISTS_GOOGLE_USER_ID

    async def test_base_login__success(
        self, auth_service: AuthService,
        get_db_session: AsyncSession
    ):
        session = get_db_session
        username = 'test_username'
        password = 'test_password'

        async with session as session:
            await session.execute(
                insert(UserProfile).values(
                    username=username,
                    password=password
                )
            )
            await session.commit()
            await session.flush()
            login_user = (await session.execute(
                select(UserProfile).where(
                UserProfile.username == username
            ))).scalar_one_or_none()

        user_data = await auth_service.login(
            username=username,
            password=password
        )

        assert login_user is not None
        assert user_data.user_id == user_data.user_id
