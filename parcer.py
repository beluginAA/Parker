from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash, phone, lastVacancy 

class Vacancies:

    def __init__(self):
        self.client = TelegramClient(phone, api_id, api_hash)
        self.client.start()
    
    @staticmethod
    def _update_last_vacancy(lastVacancy: str) -> None:
        config_file = "config.py"
        lastVacancy = lastVacancy.text

        with open(config_file, "r") as file:
            lines = file.readlines()
            found_last_vacancy, updated_lines = False, []
            
            for line in lines:
                if "lastVacancy" in line:
                    found_last_vacancy = True
                    updated_lines.append(f"lastVacancy = \'''{lastVacancy}\'''\n")
                elif not found_last_vacancy:
                    updated_lines.append(line)

        with open(config_file, "w") as file:
            file.writelines(updated_lines)

    @staticmethod
    def _get_salary(string:str) -> int:
        delimiter = " $" if '$' in string else " ₽"
        amount = string.split(delimiter)[0]
        if '—‍' in amount:
            left, right = [int(number.replace(' ', '')) for number in amount.split(' —‍ ')]
            salary = int((left+right)/2)
        else:
            salary = int(amount.replace("от", "").replace(" ", ""))
        return salary
    
    @staticmethod
    def _get_stack(string:str) -> list[str]:
        array = string.replace('**Стек**: ', '').replace('.', '').split(', ')
        correctArray = []
        for iter in array:
            if '/' not in iter:
                correctArray.append(iter)
            else:
                left,right = iter.split('/')
                array.extend([left, right])
        return correctArray
    
    @staticmethod
    def _get_value(stack: list[str], salary:int) -> dict[str:int]:
        pass

    def get(self) -> None:

        def get_vacancy(vacancy: str) -> list[str]:
            information = vacancy.text.split('\n')
            salary, stack = information[1], information[6]
            return salary, stack

        dialogs = self.client.get_dialogs() 
        for dialog in dialogs:
            if dialog.title == 'getmatch: бот с IT-вакансиями':
                messages = self.client.iter_messages(dialog)

        for message in messages:
            if message != lastVacancy:
                salary, stack = get_vacancy(message)
                correctSalary = self._get_salary(salary)
                correctStack = self._get_stack(stack)
                self._get_value(correctStack, correctSalary)
                break
            else:
                break
        
        # for message in messages:
        #     self._update_last_vacancy(message)
        #     break
    
    def describe(self) -> None:
        pass

