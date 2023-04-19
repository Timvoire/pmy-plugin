from pagermaid.listener import listener
from pagermaid.single_utils import safe_remove
from pagermaid.enums import Client, Message
from pagermaid.utils import client,pip_install
import string
import time

pip_install("deep-translator")

from deep_translator import GoogleTranslator


async def get_text(message: Message):
    if reply := message.reply_to_message:
        if reply.text:
            text = reply.text.replace("\n","")
            return text
    return ""
async def langdetect(text):
    uri = 'https://fanyi.baidu.com/langdetect'
    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    data = {
        'query': text
    }
    resp = await client.post(uri, headers=header, data=data)
    if resp.status_code==200:
        response = resp.json()
        return response['lan']
    return ""
    
async def translate(tg, text):
    language = {'zh': "en", 'en': 'zh-CN'}
    translated = GoogleTranslator(source='auto', target=language[tg]).translate(text)
    return translated

@listener(command="gt",
          description="回复一句话进行翻译")
async def audio_to_voice(bot: Client, message: Message):
    text = await get_text(message)
    if text == '':
        return await message.edit("请回复一个文本信息")
    else:   
        language = await langdetect(text)
        try:
            result = await translate(language,text)
            await message.edit(f"{result}")
        except Exception as e:
            await message.edit(f"翻译消息失败：{e}")
    
