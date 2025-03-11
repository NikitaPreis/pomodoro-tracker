from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    user_id: int

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    name: str
    description: str | None = None
