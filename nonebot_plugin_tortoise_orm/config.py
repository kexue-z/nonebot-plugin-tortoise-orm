from typing import Dict

from nonebot import get_driver
from pydantic import Extra, BaseModel, root_validator
from nonebot.log import logger
from nonebot_plugin_localstore import get_data_dir


class Config(BaseModel, extra=Extra.ignore):
    db_url: str

    @root_validator(pre=True, allow_reuse=True)
    def set_default(cls, value: Dict):
        if not value.get("db_url"):
            value["db_url"] = f'sqlite:///{get_data_dir("") / "db.sqlite3"}'
            logger.warning(f"没有设置数据库地址, 使用 {value['db_url']}")

        return value


plugin_config = Config.parse_obj(get_driver().config)
DB_URL = plugin_config.db_url
