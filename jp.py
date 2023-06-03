import urllib.parse
import asyncio
from pagermaid import Config, log
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import lang

@listener(command="jp",
          description="举牌",
          parameters="[text/reply]")
async def jp(message: Message):
    replyMode = False
    try:
      text = message.arguments
      if not text:
          if not message.reply_to_message:
              m = await message.edit(lang('arg_error'))
              await asyncio.sleep(3)
              await message.safe_delete()
              await m.safe_delete()
              return 
          text = message.reply_to_message.text
          if not text:
              m = await message.edit(lang('arg_error'))
              await asyncio.sleep(3)
              await message.safe_delete()
              await m.safe_delete()
              return 
          replyMode = True
      params = { "msg": text }
      encoded = urllib.parse.urlencode(params)
      image_url = f"http://juapi.org/api/zt.php?{encoded}"

      if replyMode:
        await message.reply_to_message.reply_photo(
          image_url
        )
      else:
        await message.reply_photo(
          image_url
        )
      await message.safe_delete()
      # user_agent_list = [
      #   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
      #   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
      #   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
      #   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
      #   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
      #   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.15'
      # ]
      # headers = {
      #   'User-Agent': random.choice(user_agent_list)
      # }
      # params = {
      #   msg: text
      # }
      # r = await client.get("http://juapi.org/api/zt.php", headers=headers, params=params, timeout=10.0)
      
      # await message.edit(f"{translated}", disable_web_page_preview=True)
      # await message.safe_delete()
    except Exception as e:
      m = await message.edit(f"失败 ~ {e}")
      await asyncio.sleep(3)
      await message.safe_delete()
      await m.safe_delete()