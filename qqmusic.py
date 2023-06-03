from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
from urllib.parse import quote
import time

header={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    
@listener(command="qq",
          description="qq音乐")
async def qq(message: Message):
    text = message.arguments
    key = quote(text,'utf-8')
    # filename = f"{text}.mp3"
    try:
        res = await client.get(f'https://zj.v.api.aa1.cn/api/qqmusic/?songName={key}&singerName=&playlistId=211111&pageNum=1&pageSize=5&type=qq',headers=header,timeout=10.0)
        if res.status_code == 200:
            resp = res.json()
            uri = resp['list'][0]['url']
            try:
                await message.reply_video(uri, caption=f"{text}", quote=False,reply_to_message_id=message.reply_to_top_message_id)
                await message.safe_delete()
            except:
                await message.edit("获取音乐失败")
            # safe_delete(filename)

    except Exception as e:
        await message.edit(message.chat_id, f"出错了呜呜呜 ~ 。{e}")
    await message.safe_delete()



