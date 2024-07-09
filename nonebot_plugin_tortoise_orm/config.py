from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    tortoise_orm_db_url: Optional[str] = None
