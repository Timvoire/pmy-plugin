from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
from pagermaid.enums import Client, Message
from urllib.parse import quote


header={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

@listener(command="tts",
          description="语音合成")
async def ghs(bot: Client, message: Message):
    text = message.arguments
    key = quote(text,encoding="utf-8")
    filename = f'{text}.mp3'
    try:
        res = await client.get(f'https://dict.youdao.com/dictvoice?audio={key}&le=zh',headers=header,timeout=10.0)
        if res.status_code == 200:
            try:
                with open(filename,'wb') as f:
                    f.write(res.content)
                    # TODO: write code...
                await bot.send_voice(message.chat.id,
            filename,reply_to_message_id=message.reply_to_top_message_id)
            except Exception as e: 
                await message.reply(e, quote=False, reply_to_message_id=message.reply_to_top_message_id)
            safe_remove(filename)
            await message.safe_delete()
    except Exception as e:
        await message.edit(message.chat_id, f"出错了呜呜呜 ~ 。{e}")
        try:
            safe_remove(filename)
        except:
            pass




