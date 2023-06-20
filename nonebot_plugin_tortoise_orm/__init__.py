from nonebot import require, get_driver

require("nonebot_plugin_localstore")
from typing import List

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

moduls: List[str] = []


@driver.on_startup
async def connect():
    await Tortoise.init(db_url=DB_URL, modules={"models": moduls})
    await Tortoise.generate_schemas()
    logger.opt(colors=True).success(
        f"<y>数据库: 连接成功</y> URL: <r>{DB_URL.split('@',maxsplit=1)[-1]}</r>"
    )


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>数据库: 断开链接</y>")


def add_model(model: str):
    logger.opt(colors=True).success(f"<y>数据库: 添加模型</y>: <r>{model}</r>")
    moduls.append(model)
