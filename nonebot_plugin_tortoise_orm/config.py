from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    db_url: str
    db_generate_schemas: bool = False
