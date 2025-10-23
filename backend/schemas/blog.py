from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    slug: str | None = None
    content: str 

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, values: dict[str, Any]):
        title = values.get('title')
        slug = values.get('slug')
        if title and slug is None:
            values['slug'] = title.replace(' ', '-').lower()
        return values

class ShowBlog(BaseModel):
    id:int
    title : str
    content:str
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateBlog(BlogCreate):
    pass
