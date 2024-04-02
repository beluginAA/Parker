from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash, expressions

class Parcer:

    def __init__(self):
        self.amountOfSkill, self.valueOfSalary = {}, {}
        self.amountOfCompanies, self.valueofCompany = {}, {}
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
            for iter in information:
                if 'на руки' in iter:
                    salary = iter
                elif '@' in iter:
                    company = iter
                elif 'Стек' in iter:
                    stack = iter
                    break
        if salary == '':
            salary = 'Вакансия без зарплаты'
        return company, salary, stack

    def _get_salary(self, string:str) -> int:
        currencies = {'₽':1, '€':99.53, '$':92.37}
        for deli in currencies.keys():
            if deli in string:
                delimiter = ' ' + deli 
                multiplier = currencies[deli]
        amount = string.split(delimiter)[0]
        if '—‍' in amount:
            left, right = [int(number.replace(' ', '').replace('\\u*d', '').replace("≈", "")) for number in amount.split(' —‍ ')]
            salary = int((left+right)/2)
        else:
            salary = int(amount.replace("от ", "").replace(" ", "").replace("≈ ", ""))
        return salary * multiplier

    def _get_company(self, company: str) -> str:
        valueList = company.split('@')[1]
        companyValue = valueList.lstrip().replace('*', '')
        return companyValue

    def _get_stack(self, string:str) -> list[str]:
        array = string.replace('**Стек**: ', '').replace('.', '').split(', ')
        correctArray = []
        for iter in array:
            if iter in expressions.keys():
                correctArray.append(expressions[iter])
            else:
                iter = [skill.lstrip().rstrip() for skill in iter.split('/')]
                correctArray.extend(iter)
        return correctArray
    
    def _get_value(self, stack: list[str], salary:int, company: str) -> dict[str:int]:
        if salary != 'Вакансия без зарплаты':
            self.valueOfSalary.setdefault(salary, [])
            self.valueOfSalary[salary].extend(stack)
        for skill in stack:
            # resultStack[skill] = cost
            self.amountOfSkill.setdefault(skill, 0)
            self.amountOfSkill[skill] += 1
        self.amountOfCompanies.setdefault(company, 0)
        self.amountOfCompanies[company] += 1
        self.valueofCompany.setdefault(company, [])
        self.valueofCompany[company].append(salary)
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
    

