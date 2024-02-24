from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash, phone, lastVacancy 

class Work:

    def __init__(self):
        self.client = TelegramClient(phone, api_id, api_hash)
        self.client.start()

    @staticmethod
    def _get_message(self, vacancy: list[str]) -> list[str]:
        information = vacancy.text.split('\n')
        content, salary, stack = information[0], information[1], information[2]
        return content, salary, stack

    def message(self) -> None:
        dialogs, vacancies = self.client.get_dialogs(), []
        for dialog in dialogs:
            if dialog.title == 'getmatch: бот с IT-вакансиями':
                messages = self.client.iter_messages(dialog)
                latestMessage = messages[0]
        
        for message in messages:
            if latestMessage != lastVacancy:
                content, salary, stack = self._get_message(message)
            else:
                lastVacancy = message
                break

