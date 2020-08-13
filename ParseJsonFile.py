import json
import time
import configparser
import asyncio
from datetime import date
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
from database import database
import warnings
warnings.filterwarnings("ignore")

testFile = open("FakesMessage.json")
data = json.load(testFile)

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)
phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)


async def getname(id):
    await client.start()
    me = await client.get_me()
    entity = PeerChannel(int(id))
    my_channel = await client.get_entity(entity)
    return(my_channel.username)


def contains_word(s, w):
    return f' {w} ' in f' {s} '


source = ""
idToChannelName1=0
n = 0
for count in data:
    # if data[n]["fwd_from"] != None:
    #     n+=1
    idToChannelName2=data[n]["to_id"]["channel_id"]
    if idToChannelName1 != idToChannelName2:
        with client:
            source = "https://t.me/" + \
                    client.loop.run_until_complete(
                        getname(data[n]["to_id"]["channel_id"]))
        idToChannelName1=idToChannelName2
    urls = ""
    i = 0
    for i in range(0, 20):
        try:
            urls += data[n]["entities"][i]["url"]+"\n"
        except KeyError:
            continue
        except IndexError:
            break
    headline = ""
    j = 0
    while(True):
        try:
            headline += data[n]["message"][j]
            j += 1
            if data[n]["message"][j] == "\n":
                break
        except IndexError:
            break
    z = 0
    hashtags = ""
    while(True):
        try:
            while(True):
                if data[n]["message"][z] == "#":
                    while(True):
                        try:
                            hashtags += data[n]["message"][z]
                            z += 1
                            if data[n]["message"][z] == " " or data[n]["message"][z] == "\n":
                                hashtags += "\n"
                                break
                        except IndexError:
                            break
                else:
                    z += 1
                if data[n]["message"][z] == "\n":
                    break
        except IndexError:
            break

    content = data[n]["message"]
    # Find message location
    location = ""
    if contains_word(content, 'ایران') or contains_word(content, 'iran'):
        location += 'ایران'+'\n'
    if contains_word(content, 'ایتالیا') or contains_word(content, 'italy'):
        location += 'ایتالیا'+'\n'
    if contains_word(content, 'چین') or contains_word(content, 'china'):
        location += 'چین'+'\n'
    if contains_word(content, 'اروپا') or contains_word(content, 'europe'):
        location += 'اروپا'+'\n'
    # Find message tags
    tags = ""
    if contains_word(content, 'امار') or contains_word(content, 'آماری'):
        tags += 'آماری'+'\n'
    if contains_word(content, 'بهداشتی'):
        tags += 'بهداشتی'+'\n'
    if contains_word(content, 'روانشناسی'):
        tags += 'روانشناسی'+'\n'
    if contains_word(content, 'درمان') or contains_word(content, 'درمانی'):
        tags += 'درمانی'+'\n'

    writingDate = data[n]["date"]
    crawlingDate = date.today()
    views = data[n]["views"]
    keywords = ""
    n += 1
    Lable=1

    db = database(#"YourHostName" ,"YourDatasetName","Username","Password")
    db.connector()
    db.cursor.execute("INSERT INTO information (headline,content,keyWords,writingDate,crawlingDate,seensCount,urls,location,hashtag,tags,source,lable) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                      (headline, content, keywords, writingDate, crawlingDate, views, urls, location, hashtags, tags, source,Lable))
    db.db.commit()
    print("Record " + str(n) + " inserted!")
