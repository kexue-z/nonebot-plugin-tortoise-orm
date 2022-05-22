from nonebot import get_driver
from tortoise import Tortoise
from nonebot.log import logger

from .config import Config

db_config = Config.parse_obj(get_driver().config.dict())
driver = get_driver()

moduls = []


@driver.on_startup
async def connect():
    await Tortoise.init(db_url=db_config.db_url, modules={"models": moduls})
    logger.opt(colors=True).success("<y>数据库: 连接成功</y>")
    if db_config.db_generate_schemas:
        logger.opt(colors=True).success("<y>数据库: 初始化</y>")
        await Tortoise.generate_schemas()


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>数据库: 断开链接</y>")


def add_model(model: str):
    moduls.append(model)
