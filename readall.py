from pagermaid.listener import listener
from pagermaid.enums import Message, Client


@listener(command="readall",
          description="查看全部未读信息", parameters="[text/reply]")
async def readall(message: Message,client: Client):
     for dialog in await client.get_dialogs_list():
        try:
            if dialog.chat.type == "ChatType.GROUP":
                await client.read_chat_history(cid)
            await message.edit("群组消息全部已读~")
        except:
            return

