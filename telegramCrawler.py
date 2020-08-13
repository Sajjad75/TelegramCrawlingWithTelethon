#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import json
import asyncio
from datetime import date, datetime
from telethon import functions, types
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# Json date and time converter
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Config file
config = configparser.ConfigParser()
config.read("config.ini")

# setting value for authentication
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# making client to communicate with Telegram
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Check whether the authentication has been done or not?
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    # Read Channel name from file
    channelLis=open('confirmedChannelsList.txt','r')
    for channel in channelLis:
        if channel.isdigit():
            entity = PeerChannel(int(channel))
        else:
            entity = channel

        my_channel = await client.get_entity(entity)
        print(str(channel))
        offset_id = 0
        limit = 1
        all_messages = []
        total_messages = 0
        total_count_limit = 0
        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await client(functions.messages.SearchRequest(
            peer=my_channel,
            q='کرونا',
            filter=types.InputMessagesFilterEmpty(),
            # limited date because Covid-19 is a new problem
            min_date=datetime(2019, 7, 1),
            max_date=datetime(2020, 3, 30),
            offset_id=offset_id,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0,
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        with open('FakesMessage.json', 'a') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)

with client:
    client.loop.run_until_complete(main(phone))