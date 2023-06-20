from typing import List

from nonebot import require, get_driver
from tortoise import Tortoise
from nonebot.log import logger

from .config import DB_URL

require("nonebot_plugin_localstore")
driver = get_driver()

moduls: List[str] = []


@driver.on_startup
async def connect():
    await Tortoise.init(db_url=DB_URL, modules={"models": moduls})
    await Tortoise.generate_schemas()
    logger.opt(colors=True).success("<y>数据库: 连接成功</y>")


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>数据库: 断开链接</y>")


def add_model(model: str):
    logger.opt(colors=True).success(f"<y>数据库: 添加模型</y>: <r>{model}</r>")
    moduls.append(model)
