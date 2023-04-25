from pagermaid.listener import listener
from pagermaid.enums import Client, Message
from pagermaid.single_utils import sqlite

@listener(command="dz",
          description="点赞")

async def dz_set(bot:Client,message:Message):
    uid = message.arguments
    sqlite[f'dz.{uid}'] = str(uid)
    await message.edit(uid)

@listener(is_plugin=True, incoming=True, ignore_edited=True)
async def dianzan(bot: Client, message: Message):
    try:
        cid = sqlite.get(f'dz.{message.from_user.id}', None)
        await message.forward(str(cid))
        if message.from_user.id == int(cid):
            await bot.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji="🔥",
        )
    except Exception as e:
        await message.edit(e[:200])