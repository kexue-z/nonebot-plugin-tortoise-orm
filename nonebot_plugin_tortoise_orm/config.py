from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    tortoise_orm_db_url: Optional[Path] = None
