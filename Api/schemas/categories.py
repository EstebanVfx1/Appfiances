from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_name: str
    category_description: str

class CategoryCreate(CategoryBase):
    category_status: bool = True

class CategoryRead(CategoryBase):
    category_id: int
    category_status: bool = True

class CategoryDelete(BaseModel):
    category_id: int