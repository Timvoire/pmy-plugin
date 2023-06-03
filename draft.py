# encoding=utf-8
import random
import urllib.parse
from urllib.parse import quote
# from pagermaid.single_utils import safe_remove
from pagermaid.listener import listener
from pagermaid.enums import Message,Client
from pagermaid.utils import client
import time
import copy
import os


''' 
个人使用 
'''
header = {
    'Host':'api.draft.art',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryTNqhKLixYKC8khXl',
    'GRAPH-ORIGIN-T': '22e47648ef454f8282b783ebb6e58e8b'
}

async def check():
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    uri = 'https://api.draft.art/api/auth/loginInfo'
    try:
        res = await client.post(uri,headers=header)
        if res.status_code ==200:
            resp = res.json()
            if resp['code'] ==200000:
                return "签到成功"

    except Exception as e:
        pass
    return "签到失败"

async def checkin():
    header['Content-Type'] = 'application/json'
    uri = 'https://pay.draft.art/api/member/getDailyBalance'
    platformBalance=""
    try:
        res = await client.get(uri, headers=header)
        # await message.edit(res.text)
        if res.status_code == 200:
            resp = res.json()
            platformBalance = resp['data']['platformBalance']
    except Exception as e:
        await message.edit(f"err log : {e}")
    return platformBalance

async def query():
    platformBalance = await checkin()
    header['Content-Type'] = 'application/json'
    uri = 'https://pay.draft.art/api/wallet/get'
    amount = ''
    try:
        res = await client.get(uri, headers=header)
        if res.status_code == 200:
            resp = res.json()
            amount = resp['data']['amount']
    except Exception as e:
        await message.edit(f"err log : {e}")
    return amount,platformBalance
        
async def get_url(iid):
    url = ''
    uri = 'https://api.draft.art/api/util/aiDraw/get/' + str(iid)
    i = 0
    while i<20:
        r = await client.post(uri, headers=header)
        if r.status_code ==200:
            result = r.json()
            status = result['data']['status']
            if status == 'succeeded':
                url = result['data']['download']
                break
        else:
            i+=1
            time.sleep(1)
    return url

async def get_image(message,text):
    filename = f"{text}.jpg"
    uri = f'https://api.draft.art/api/util/aiDraw/createByTemplate?keyword={text}&height=1024&width=512&initImage=&language=zh&templateId=100003'
    res = await client.post(uri,headers=header)
    if res.status_code == 200:
        resp = res.json()
        iid = resp['data']['id']
        # await message.edit(str(iid)) 
        # time.sleep(3)
        url = await get_url(iid)
        # await message.edit(url)
        try:
            resp = await client.get(url)
            with open(filename,'wb') as f:
                f.write(resp.content)
                await message.reply_photo(filename, quote=False,reply_to_message_id=message.reply_to_message_id
            or message.reply_to_top_message_id)
            os.remove(filename)
            await message.safe_delete()
        except Exception as e:
            await message.edit(f"获取图片异常 :{e}")
       
    
@listener(command="d",
          description="AI画图",parameters="[text/reply]")
async def kw(message: Message):
    text = message.arguments
    l = ['help','签到','查询']
    if text !="":
        if  text not in l:
            await get_image(message, text)
            
        if text == "help":
            await message.edit("插件有3个功能，每天可以签到 命令是  d 签到”,可以领取10次\n查询 命令是 d 查询”,查看当前账户可用次数\n 第三个是ai绘画，命令是 d text")
        if text == "签到":
            result = await check() 
            await message.edit(result)
        if text == '查询':
            amount,platformBalance = await query()
            await message.edit(f"查询成功：剩余 {amount} 次 免费次数剩余 {platformBalance} 次")

            
            
        
    else:
        await message.edit("输入点什么吧 要不祝我开心也行~")
        
    
    