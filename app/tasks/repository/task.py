from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.tasks.models import Category, Task
from app.tasks.schema import TaskSchema, TaskCreateSchema


class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self, user_id: int):
        query = select(Task).where(Task.user_id == user_id)
        async with self.db_session as session:
            tasks: list[Task] = (await session.execute(
                query
            )).scalars().all()
        return tasks

    async def get_task(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def get_user_task(self, task_id: int, user_id: int):
        query = select(Task).where(
            Task.id == task_id, Task.user_id == user_id
        )
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
            return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = insert(Task).values(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        ).returning(Task.id)
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one()
            await session.commit()
            return task_id

    async def delete_task(self, task_id: int, user_id: int) -> Task:
        query = delete(Task).where(
            Task.id == task_id, Task.user_id == user_id
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_tasks_by_category_name(
        self, category_name: str
    ) -> list[Task]:
        query = select(Task).join(
            Category, Task.category_id == Category.id
        ).where(
            Category.name == category_name
        )
        async with self.db_session as session:
            task: list[Task] = (await session.execute(
                query
            )).scalars().all()
        return task
    
    async def update_task_name(
            self, task_id: int, name: str
    ) -> Task:
        query = update(Task).where(Task.id == task_id).values(
            name=name
        ).returning(Task.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(
                query
            )).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)
