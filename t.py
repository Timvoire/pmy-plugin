from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
from pagermaid.enums import Client, Message
from urllib.parse import quote
import base64,os


header={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

@listener(command="t",
          description="语音合成")
async def ghs(bot: Client, message: Message):
    text = message.arguments
    filename = f'{text}.ogg'
    try:
        data = {'text': text, 'speaker': "tts.other.BV021_streaming", 'language': "zh"}
        res = await client.post('https://translate.volcengine.com/web/tts/v1/',headers=header,json=data,timeout=10.0)
        if res.status_code == 200:
            try:
                resp = res.json()
                audio = resp['audio']['data']
                audio = base64.b64decode(audio)
                with open(filename,'wb+') as f:
                    f.write(audio)
                    # TODO: write code...
                await bot.send_voice(message.chat.id,
            filename,reply_to_message_id=message.reply_to_top_message_id)
            except Exception as e: 
                await message.reply(e, quote=False, reply_to_message_id=message.reply_to_top_message_id)
            os.remove(filename)
    except Exception as e:
        await message.edit(f"出错了呜呜呜 ~ 。{e}")
    safe_remove(filename)


   
    

