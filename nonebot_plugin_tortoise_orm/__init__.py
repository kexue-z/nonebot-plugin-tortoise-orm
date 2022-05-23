from typing import List

from nonebot import get_driver
from tortoise import Tortoise
from nonebot.log import logger

from .config import Config

db_config = Config.parse_obj(get_driver().config.dict())
driver = get_driver()

db_url = db_config.db_url

if not db_url or "":
    logger.opt(colors=True).warning("<y>没有数据库地址, 将会初始化数据库到 db.sqlite3</y>")
    db_url = "sqlite://db.sqlite3"

moduls: List[str] = []


@driver.on_startup
async def connect():

    await Tortoise.init(db_url=db_url, modules={"models": moduls})
    await Tortoise.generate_schemas()
    logger.opt(colors=True).success("<y>数据库: 连接成功</y>")


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>数据库: 断开链接</y>")


def add_model(model: str):
    logger.opt(colors=True).success(f"<y>数据库: 添加模型</y>: <r>{model}</r>")
    moduls.append(model)
