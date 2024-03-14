from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash
from last_vacancy import lastVacancy 

class Parcer:

    def __init__(self):
        self.amountOfSkill = {}
        self.amountOfVacancions = 0
        self.client = TelegramClient('test_tg', api_id, api_hash)
        self.client.start()

    def _get_dialogs(self) -> list[str]:
        dialogs = self.client.get_dialogs() 
        for dialog in dialogs:
            if dialog.title == 'getmatch: бот с IT-вакансиями':
                messages = self.client.iter_messages(dialog)
                break
        return messages

    def _get_info(self, vacancy: str, salary = '', stack = '') -> list[str]:
        information = vacancy.text.split('\n')
        if len(information) > 5:
            salary, stack = information[1], information[6]
        return salary, stack

    def _get_salary(self, string:str) -> int:
        delimiter = " $" if '$' in string else " ₽"
        amount = string.split(delimiter)[0]
        if '—‍' in amount:
            left, right = [int(number.replace(' ', '').replace('\\u*d', '').replace("≈", "")) for number in amount.split(' —‍ ')]
            salary = int((left+right)/2)
        else:
            salary = int(amount.replace("от ", "").replace(" ", "").replace("≈ ", ""))
        return salary
    
    def _get_stack(self, string:str) -> list[str]:
        array = string.replace('**Стек**: ', '').replace('.', '').split(', ')
        exceptions = ['CI/CD', 'TCP/IP']
        correctArray = []
        for iter in array:
            iter = iter.lstrip().rstrip()
            if iter == 'NET 31/6':
                correctArray.append('NET 3.1/6')
            elif iter == 'Gitlab CI':
                correctArray.append('CI/CD')
            elif iter in ['Ubuntu', 'Debian']:
                correctArray.append('Linux')
            elif iter == 'HaProxy':
                correctArray.append('HAProxy')
            elif iter == 'Hashicorp Vault':
                correctArray.append('HashiСorp Vault')
            elif iter == 'MS SQL':
                correctArray.append('Microsoft SQL Server')
            elif iter in ['TCP', 'IPv4']:
                correctArray.append('TCP/IP')
            elif iter == 'TerraForm':
                correctArray.append('Terraform')
            elif iter == 'Apache Kafka':
                correctArray.append('Kafka')
            elif iter in ['tcpdump', 'vSphere']:
                correctArray.append(iter[0].upper() + iter[1:])
            elif ('/' not in iter) or (iter in exceptions):
                correctArray.append(iter)
            else:
                iter = [skill.lstrip().rstrip() for skill in iter.split('/')]
                correctArray.extend(iter)
        return correctArray
    
    def _get_value(self, stack: list[str], salary:int) -> dict[str:int]:
        cost = salary / len(stack)
        for skill in stack:
            # resultStack[skill] = cost
            self.amountOfSkill.setdefault(skill, 0)
            self.amountOfSkill[skill] += 1
        # return stack
    
    @staticmethod
    def _update_last_vacancy(lastVacancy: str) -> None:
        config_file = "last_vacancy.py"
        lastVacancy = lastVacancy.text

        with open(config_file, "r") as file:
            lines = file.readlines()
            updated_lines = []
    
            for line in lines:
                if "lastVacancy" not in line:
                    updated_lines.append(line)
                else:
                    updated_lines.append(f"lastVacancy = \'''{lastVacancy}\'''\n")
                    break

        with open(config_file, "w") as file:
            file.writelines(updated_lines)

    def _get_last_vacancy(self, messages: list[str]) -> None:
        for message in messages:
            self._update_last_vacancy(message)
            break
    

