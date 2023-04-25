from pagermaid.listener import listener
from pagermaid.enums import Client, Message
from pagermaid.single_utils import sqlite


@listener(command="dz",
          description="点赞")
async def dz_set(bot: Client, message: Message):
    try:
        if len(message.parameter) != 2:
            await message.edit("格式错误")
        else:
            uid = message.parameter[-1]
            if message.parameter[0] == "set":
                sqlite[f'dz.{uid}'] = str(uid)
                await message.edit("设置成功")
            if message.parameter[0] == "del":
                del sqlite[f'dz.{uid}']
                await message.edit("删除成功")
    except Exception as e:
        return


@listener(is_plugin=True, incoming=True, ignore_edited=True)
async def dianzan(bot: Client, message: Message):
    try:
        cid = sqlite.get(f'dz.{message.from_user.id}', None)
        if not cid:
            return
        if message.from_user.id == int(cid):
            await bot.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji="🐳",
            )
    except Exception as e:
        return
