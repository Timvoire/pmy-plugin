# encoding=utf-8
import random
import urllib.parse
from urllib.parse import quote
from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
import time
import os

''' 
个人使用 
'''


async def get_video_url(text):
    header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'https://draft.art/',
    'Content-Type': 'application/json'
}
    uri = 'https://api.draft.art/api/util/image/listCommunity'
    data={
    "size": 30,
    "current": 1,
    "search": f"{text}",
    "mode": "community",
    "needCollectStatus": True
}
    resp = await client.post(uri, headers=header,json=data)
    if resp.status_code == 200:
        response = resp.json()
        result = response['data']['records']
        i = random.randint(0,len(result)-1)
        try:
            url = result[i]['url']
        except:
            pass
    else:
        pass
    return url


@listener(command="draw",
          description="画图",parameters="[text/reply]")
async def kw(message: Message):
    text = message.arguments
    try:
        url = await get_video_url(text)
        filename = f"{text}.jpg"
        try:
            resp = await client.get(url)
            with open(filename,'wb') as f:
                f.write(resp.content)
            await message.reply_photo(filename,quote=False, reply_to_message_id=message.reply_to_message_id
            or message.reply_to_top_message_id)
            
            os.remove(filename)
            await message.safe_delete()
        except Exception as e:
            await message.safe_delete()
            await message.edit(f"发送失败,{str(e)}")
    except Exception as e:
        await message.edit(e[:200])
    await message.safe_delete()
    




