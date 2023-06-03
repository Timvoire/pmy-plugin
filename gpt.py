from pagermaid.listener import listener
from pagermaid.single_utils import safe_remove
from pagermaid.enums import Client, Message
from pagermaid.utils import client,pip_install
import string
import time


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
    
async def chat(text):
    uri = f'https://v1.apigpt.cn/?q={text}&apitype=sql'
    res = await client.get(uri,timeout=60.0)
    if res.status_code ==200:
        resp = res.json()
        return resp['ChatGPT_Answer']
    return ""

@listener(command="ai",
          description="chatgpt聊天")
async def audio_to_voice(bot: Client, message: Message):
    text = message.arguments
    if text == '':
        return await message.edit("请输入文本信息")
    else:   
        result = await chat(text)
        if result != "":
            await message.reply_text(result,quote=True)
        await message.edit("获取结果为空~")
    
