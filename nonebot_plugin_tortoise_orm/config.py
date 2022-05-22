from typing import Optional

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    db_url: Optional[str]
