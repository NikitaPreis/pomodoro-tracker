from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from schema import UserCreateSchema
from models import UserProfile


@dataclass
class UserRepository:
    db_session: Session

    def create_user(
        self, user: UserCreateSchema
    ) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump(),
        ).returning(UserProfile.id)
        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            print('create_user_id', user_id)
            return self.get_user(user_id)

    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
           return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.username == username
        )
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_email(self, email: str):
        query = select(UserProfile).where(
            UserProfile.email == email
        )
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def get_google_user(self, google_token: str) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.google_access_token == google_token
        )
        with self.db_session() as session:
            user = session.execute(query).scalar_one_or_none()
            print(user)
            return user
