from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    tortoise_orm_db_url: Optional[Union[Path, str]] = None
