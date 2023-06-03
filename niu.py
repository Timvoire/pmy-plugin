from pyrogram import Client, enums

import re
import random
import asyncio
from pagermaid.listener import listener
from pyrogram.types import InputMediaPhoto
from pagermaid.services import client as requests
from pagermaid.enums import Message, Client

@listener(command="lsp", description="lsp 末尾添加 `s` 将启用防剧透功能",
          parameters="[自定义频道] [s]")
async def lsp(client: Client, message: Message):
    try:
        # print(message)
        fromUserId = message.from_user.id
        # print(fromUserId)
        # me = await client.get_me()
        # userId = me.id
        p = message.parameter
        channel = None
        channels = [
            "meinvbaike", # 美女百科 
        ]
        spoiler = False
        if len(p) == 0:
            channel = random.choice(channels)
        elif len(p) == 1:
            if p[0] == 's':
                # s
                spoiler = True
                channel = random.choice(channels)
            else:
                # channel
                channel = p[0]
        elif len(p) == 2:
            spoiler = True
            channel = p[0]
        else:
            await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
            return
        # print(channel)
        # print(spoiler)
        if spoiler == True:
            caption = '||'
        else:
            caption = ''
        chat_id = message.chat.id
        reply = message.reply_to_message_id if message.reply_to_message_id else None


        m = await message.edit(f'[获取图片中...](https://t.me/{channel})', disable_web_page_preview=True)
        # print(m)
        userId = m.from_user.id
        # print(m)
        if userId != fromUserId:
            message = m

        count = await client.search_messages_count(chat_id=channel, filter=enums.MessagesFilter.IMAGE)
        random_offset = random.randint(1, count)
        await message.edit(f'[获取图片中 {random_offset}/{count}...](https://t.me/{channel})', disable_web_page_preview=True)
        v = None
        async for m in client.search_messages(chat_id=channel, offset=random_offset, limit=1, filter=enums.MessagesFilter.IMAGE):
            v = m
            await message.edit(f'[获取涩涩图片...](https://t.me/{channel}/{m.id})', disable_web_page_preview=True)
            if spoiler:
                video = await client.download_media(m.image.file_id, in_memory=True)
            else:
                video = m.image.file_id
            await message.reply_video(video, caption=f'[涩涩 {random_offset}/{count}](https://t.me/{channel}/{m.id})', has_spoiler=spoiler)
        if v:
            await message.safe_delete()
        else:
            await message.edit(f'[找不到涩涩...](https://t.me/{channel})', disable_web_page_preview=True)
    except Exception as e:
        await message.edit(f"涩涩失败 ~ {e}")
        