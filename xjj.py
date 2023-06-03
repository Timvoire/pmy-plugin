from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message,Client
from pagermaid.utils import client as request
import time
import random

def get_url(url_list):
    url = url_list['data'][0]['hoverUrl']
    return url

@listener(command="xjj",
          description="小姐姐写真")
async def ghs(message: Message, client: Client):
    await message.edit("拍小姐姐写真中 . . .")
    status = False
    filename = "xjj.jpg"
    try:
        i = random.randint(0,100)
        img = await request.get(f"https://zj.v.api.aa1.cn/api/so-baidu-img/?msg=美女&page={i}",timeout=10.0)
        if img.status_code == 200:
            url = get_url(img.json())
            res = await request.get(url,timeout=10.0)
            with open(filename, 'wb') as f:
                f.write(res.content)
            await message.edit("写真我拍好辣，上传中 . . .")
            try:
                await message.reply_photo(filename, caption="", reply_to_message_id=message.reply_to_top_message_id)
            except Exception as e: 
                await message.reply_photo(e, quote = False, reply_to_message_id=message.reply_to_top_message_id)
            # import os
            # os.remove(filename)
            await message.safe_delete()
    except Exception as e:
        await message.edit(f"出错了呜呜呜 ~ {e}。")
