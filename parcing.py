from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash, phone

import csv

client = TelegramClient(phone, api_id, api_hash)
client.start()

dialogs = client.get_dialogs()
for dialog in dialogs:
    if dialog.title == 'getmatch: бот с IT-вакансиями':
        messages = client.iter_messages(dialog)

for message in messages:
    i = message.text.split('\n')
    print(i)
    break

