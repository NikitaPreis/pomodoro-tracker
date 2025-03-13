from typing import Optional

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.core.categories.models import Category
from app.core.tasks.models import Task


class CategoryFilter(Filter):
    name: Optional[str] = Field(default=None)

    class Constants(Filter.Constants):
        model = Category


class TaskFilter(Filter):
    name: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    category: Optional[CategoryFilter] = FilterDepends(
        with_prefix('category', CategoryFilter
    ))

    class Constants(Filter.Constants):
        model = Task

    class Config:
        allow_population_by_field_name = True
