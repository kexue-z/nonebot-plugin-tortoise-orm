from nonebot import get_driver, require

require("nonebot_plugin_localstore")
from json import dumps
from pathlib import Path
from typing import List, Optional

import nonebot_plugin_localstore as store
from nonebot import get_plugin_config
from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from tortoise import Tortoise

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_tortoise_orm",
    description="Tortoise ORM 插件",
    usage="看文档",
    type="library",
    homepage="https://github.com/kexue-z/nonebot-plugin-tortoise-orm",
    config=Config,
)

plugin_config = get_plugin_config(Config)

plugin_data_file: Path = store.get_data_file(
    "nonebot_plugin_tortoise_orm", "db.sqlite3"
)


db_url = (
    "sqlite:///" + str(plugin_data_file)
    if plugin_config.tortoise_orm_db_url is None
    else plugin_config.tortoise_orm_db_url
)


driver = get_driver()


DATABASE = {
    "connections": {"default": db_url},
    "apps": {
        "default": {
            "models": [],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}

models: List[str] = []


@driver.on_startup
async def connect():
    # await Tortoise.init(db_url=DB_URL, modules={"models": moduls})
    DATABASE["apps"]["default"]["models"] = models

    logger.debug("参数预览\n" + dumps(DATABASE, ensure_ascii=False, indent=4))

    await Tortoise.init(DATABASE)
    await Tortoise.generate_schemas()

    for db in DATABASE["connections"].keys():
        db_url = DATABASE["connections"][db].split("@", maxsplit=1)[-1]
        logger.opt(colors=True).success(
            f"<y>数据库: {db} 连接成功</y> URL: <r>{db_url}</r>"
        )


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>数据库: 断开链接</y>")


def add_model(model: str, db_name: Optional[str] = None, db_url: Optional[str] = None):
    """
    :说明: `add_model`
    > 添加数据模型

    :参数:
      * `model: str`: 模型位置/名称
            - 如果发布插件可以为 `__name__` 或 插件名称.模型所在文件 例如 `abc.models`
            - 如果是作为 Bot 插件形式 需按照相对路径填写 例如 `plugins.test.models`

    :可选参数: 该可选参数必须同时使用

    仅在需要自定义某插件独立数据库时需要，否则将会使用默认 `db_url` 存放在默认位置

      * `db_name: Optional[str] = None`: 数据库名称
      * `db_url: Optional[str] = None`: 数据库URL [参考](https://tortoise.github.io/databases.html#db-url)
    """
    if bool(db_name) != bool(db_url):
        raise TypeError("db_name 和 db_url 必须同时为 None 或 str")

    if db_name and db_url:
        DATABASE["connections"][db_name] = db_url
        DATABASE["apps"][db_name] = {"models": []}
        DATABASE["apps"][db_name]["default_connection"] = db_name
        DATABASE["apps"][db_name]["models"].append(model)
        logger.opt(colors=True).success(
            f"<y>数据库: 添加模型 {db_name}</y>: <r>{model}</r>"
        )

    else:
        models.append(model)
        logger.opt(colors=True).success(f"<y>数据库: 添加模型</y>: <r>{model}</r>")
