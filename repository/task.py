from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import Category, Task
from schema.tasks import TaskSchema


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        query = select(Task)
        with self.db_session() as session:
            tasks: list[Task] = session.execute(query).scalars().all()
        return tasks

    def get_task(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        with self.db_session() as session:
            task = session.execute(query).scalar_one_or_none()
        return task

    def create_task(self, task: TaskSchema) -> int:
        task_model = Task(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id
        )
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def delete_task(self, task_id: int) -> Task:
        query = delete(Task).where(Task.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Task]:
        query = select(Task).join(
            Category, Task.category_id == Category.id
        ).where(
            Category.name == category_name
        )
        with self.db_session as session:
            task: list[Task] = session.execute(query).scalars().all()
        return task
    
    def update_task_name(
            self, task_id: int, name: str
    ) -> Task:
        query = update(Task).where(Task.id == task_id).values(
            name=name
        ).returning(Task.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
