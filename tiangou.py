from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
import time


header={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

@listener(command="tg",
          description="舔狗日记")
async def ghs(message: Message):
    try:
        res = await client.get('https://v.api.aa1.cn/api/tiangou/index.php',headers=header,timeout=10.0)
        if res.status_code == 200:
            resp = res.text
            try:
                await message.edit("🐶舔狗日记："+resp)
            except Exception as e: 
                pass
    except Exception as e:
        await message.edit(message.chat_id, f"出错了呜呜呜 ~ 。{e}")



