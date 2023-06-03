from secrets import choice
from pagermaid.listener import listener
from pagermaid.enums import Message


@listener(command="c",
          description="")
async def crazy4(message: Message):
    if reply := message.reply_to_message:
        await message.edit(str(reply))
