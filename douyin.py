# encoding=utf-8
import random
import urllib.parse
from urllib.parse import quote
from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.utils import client as request
from pagermaid.enums import Message, Client
import time
import os

''' 
个人使用 
搜索抖音视频 先下载后发送
'''


async def get_video_url(r):
    header = {
    'cookie': '',
    'Referer': f'https://www.douyin.com/search/{r}?publish_time=0&sort_type=0&source=switch_tab&type=video',
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
    uri = f'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=2&publish_time=0&keyword={r}&search_source=tab_search&query_correct_type=1&is_filter_search=1&from_group_id=&offset=0&count=30&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=107.0.0.0&browser_online=true&engine_name=Blink&engine_version=107.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=150&webid=7144169315942827524&msToken=CVyqfmnwaKH4O-eSURDSuXWS6hTVX6ycMgbhs5ourenaflGbmPsS9XhYcKcgH0xNlwrHIkOBWqsZ54IftAjrjXDwK2sa90bh-U8dYoJtSFBfaZbEuj1dhErqbCp6ZGeK&X-Bogus=DFSzswVu9PzAN9jstVXpCr7TlqtX'

    resp = await request.get(uri, headers=header)
    url = ''
    desc = ''
    if resp.status_code == 200:
        response = resp.json()
        result = response['data']
        i = random.randint(0,len(result)-1)
 
        try:
            # print(i)
            info = result[i]['aweme_info']
            desc = info['desc']
            url = info['video']['play_addr']['url_list'][0]
        except:
            pass
    else:
        pass
    return url,desc


@listener(command="dy",
          description="dy视频",parameters="[text/reply]")
async def kw(message: Message,client:Client):
    text = message.arguments
    await message.edit(f"查找视频 '{text}' 中...")
    try:
        key = quote(text,'utf-8')
        url,desc = await get_video_url(key)
        filename = f"{text}.mp4"
        try:
            resp = await request.get(url)
            with open(filename,'wb') as f:
                f.write(resp.content)
            # await message.reply_video(filename, caption=desc, quote=False,has_spoiler=True)
                await client.send_animation(chat_id=message.chat.id, animation=filename)
            os.remove(filename)
            # await message.safe_delete()
        except:
            await message.safe_delete()
            return
    except Exception as e:
        return
    await message.safe_delete()
    




