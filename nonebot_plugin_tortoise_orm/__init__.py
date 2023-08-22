from nonebot import require, get_driver

require("nonebot_plugin_localstore")
from json import dumps
from typing import List, Optional

from tortoise import Tortoise
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import DB_URL, Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_tortoise_orm",
    description="Tortoise ORM 插件",
    usage="看文档",
    type="library",
    homepage="https://github.com/kexue-z/nonebot-plugin-tortoise-orm",
    config=Config,
)

driver = get_driver()


DATABASE = {
    "connections": {"default": DB_URL},
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
        logger.opt(colors=True).success(f"<y>数据库: {db} 连接成功</y> URL: <r>{db_url}</r>")


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
        logger.opt(colors=True).success(f"<y>数据库: 添加模型 {db_name}</y>: <r>{model}</r>")

    else:
        models.append(model)
        logger.opt(colors=True).success(f"<y>数据库: 添加模型</y>: <r>{model}</r>")
