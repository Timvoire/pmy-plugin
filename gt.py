from pagermaid.listener import listener
from pagermaid.single_utils import safe_remove
from pagermaid.enums import Client, Message
from pagermaid.utils import client
import time


async def get_text(message: Message):
    if reply := message.reply_to_message:
        if reply.text:
            text = reply.text.replace("\n",',')
            return text
    return ""


async def translate(text):
    uri = f'https://v.api.aa1.cn/api/api-fanyi-yd/index.php?msg={text}&type=3'
    res = await client.get(uri, timeout=10.0)
    if res.status_code == 200:
        text = res.json()['text']
        return text
    return ""


@listener(command="gt",
          description="回复一句话进行翻译")
async def audio_to_voice(bot: Client, message: Message):
    text = await get_text(message)
    if text == '':
        return await message.edit("请回复一个文本信息")
    else:
        try:
            result = await translate(text)
            await message.edit(f"翻译结果：{result}")
        except Exception as e:
            await message.edit(f"翻译消息失败：{e}")

