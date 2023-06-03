# encoding=utf-8
import urllib.parse
from urllib.parse import quote
from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import client
import time

''' 
1\获取音乐列表

2\获取音乐url

3、下载音乐

'''


async def get_music_list(name):
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1679151013; _ga=GA1.2.805612427.1679151014; _gid=GA1.2.118929939.1679151014; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1679151177; kw_token=82EYFLLB2FY',
    'csrf': '82EYFLLB2FY',
    'Referer': f'https://www.kuwo.cn/search/list?key={name}'
    }
    url = f'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={name}&pn=1&rn=20&httpsStatus=1'
    resp = await client.get(url, headers=header,timeout=10)
    if resp.status_code == 200:
        response = resp.json()
        musicid = response['data']['list']
    else:
        musicid = 0
    return musicid


async def get_music_url(musicid,name):
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1679151013; _ga=GA1.2.805612427.1679151014; _gid=GA1.2.118929939.1679151014; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1679151177; kw_token=82EYFLLB2FY',
    'csrf': '82EYFLLB2FY',
    'Referer': f'https://www.kuwo.cn/search/list?key={name}'
    }
    for id in musicid:
        rid = id['rid']
        url = f'https://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=music&httpsStatus=1'
        resp = await client.get(url, headers=header,timeout=10)
        if resp.status_code == 200:
            if resp.json()['code'] == 200:
                resp = resp.json()
                mp3 = resp['data']['url']
                break
    else:
        mp3=''
    
    return mp3


@listener(command="kw",
          description="酷我音乐",parameters="[text/reply]")
async def kw(message: Message):
    text = message.arguments
    await message.edit(f"查找音乐 '{text}' 中...")
    try:
        key = quote(text,'utf-8')
        music = await get_music_list(key)
        url = await get_music_url(music,key)
        try:
            await message.reply_video(url, caption=text, quote=False,reply_to_message_id=message.reply_to_top_message_id)
            
        
            # await message.safe_delete()
        except:
            await message.edit("发送失败")
    except Exception as e:
        await message.edit(e)
    # await message.safe_delete()




