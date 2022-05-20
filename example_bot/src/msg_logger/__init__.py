from nonebot import on_command, on_message
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot_plugin_tortoise_orm import add_model

from .models import LogForm

add_model("src.msg_logger.models")
msg = on_message(priority=1, block=False)


@msg.handle()
async def _(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        await LogForm.update_or_create(
            message_id=event.message_id,
            user_id=event.user_id,
            group_id=event.group_id,
            time=event.time,
            message=event.get_message(),
            data=event.json(),
        )
    elif isinstance(event, PrivateMessageEvent):
        await LogForm.update_or_create(
            message_id=event.message_id,
            user_id=event.user_id,
            group_id=None,
            time=event.time,
            message=event.get_message(),
            data=event.json(),
        )


lookup_msg = on_command("查询记录")


@lookup_msg.handle()
async def _(qid: Message = CommandArg()):
    try:
        user_id = int(qid.extract_plain_text().strip())
    except ValueError:
        await lookup_msg.finish("id不对")

    msg = f"# 查询 {user_id} 结果\n\n- `群`: `内容`\n"
    if logs := await LogForm.filter(user_id=user_id).values():
        i = 0
        for log in logs:
            template = "- `{group_id}`: {message}\n"
            msg += template.format(**log)
            i += 1
            if i >= 30:
                break
        # await lookup_msg.finish(message=MessageSegment.image(await md_to_pic(msg)))

        # 只会在 debug 里面输出
        logger.debug(msg)
