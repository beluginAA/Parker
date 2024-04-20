from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from loguru import logger

from config import api_id, api_hash, expressions
from mysql import Mysql
from last_vacancy import lastVacancy 

import sys

class Parcer:

    logger.remove()
    loggerParcer = logger.bind(key = 'ParcerLpgger').opt(colors = True)
    loggerParcer.add(sink = sys.stdout, format = "<green>{time:HH:mm:ss}</green> | {message}", level = 'INFO')

    def __init__(self):
        self.amountOfSkill, self.valueOfSalary = {}, {}
        self.amountOfCompanies, self.valueofCompany, self.valueofCompanyForeign = {}, {}, {}
        self.amountOfVacancions = 0
        self.client = TelegramClient('test_tg', api_id, api_hash)
        self.client.start()

    def _get_dialogs(self) -> list[str]:
        Parcer.loggerParcer.info('Connecting to telegram-bot')
        dialogs = self.client.get_dialogs() 
        for dialog in dialogs:
            if dialog.title == 'getmatch: бот с IT-вакансиями':
                messages = self.client.iter_messages(dialog)
                break
        return messages

    def _get_info(self, vacancy: str, salary = '', stack = '', company = '') -> list[str]:
        Parcer.loggerParcer.info('Getting information about vacancy.')
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

    def _get_salary(self, string:str) -> list[int, str]:
        Parcer.loggerParcer.info('Getting vacancy salary.')
        currencies = {'₽':1, '€':99.53, '$':92.37}
        for deli in currencies.keys():
            if deli in string:
                delimiter = ' ' + deli 
                multiplier = currencies[deli]
                currency = deli
        amount = string.split(delimiter)[0]
        if '—‍' in amount:
            left, right = [int(number.replace(' ', '').replace('\\u*d', '').replace("≈", "")) for number in amount.split(' —‍ ')]
            salary = int((left+right)/2)
        else:
            salary = int(amount.replace("от ", "").replace(" ", "").replace("≈ ", ""))
        return salary, currency

    def _get_company(self, company: str) -> str:
        Parcer.loggerParcer.info('Getting information about company.')
        valueList = company.split('@')[1]
        companyValue = valueList.lstrip().replace('*', '').rstrip()
        return companyValue

    def _get_stack(self, string:str) -> list[str]:
        Parcer.loggerParcer.info('Getting information about skills.')
        array = string.replace('**Стек**: ', '').replace('.', '').split(', ')
        correctArray = []
        for iter in array:
            if iter in expressions.keys():
                correctArray.append(expressions[iter])
            else:
                iter = [skill.lstrip().rstrip() for skill in iter.split('/')]
                correctArray.extend(iter)
        return correctArray
    
    def _get_value(self, stack: list[str], salary:int, currency: str, company: str) -> dict[str:int]:
        Parcer.loggerParcer.info('Working on value of vacancy.')
        if (salary != 'Вакансия без зарплаты') and (currency == '₽'):
            self.valueOfSalary.setdefault(salary, [])
            self.valueOfSalary[salary].extend(stack)
        for skill in stack:
            # resultStack[skill] = cost
            self.amountOfSkill.setdefault(skill, 0)
            self.amountOfSkill[skill] += 1
        if 'Название скрыто' not in company:
            self.amountOfCompanies.setdefault(company, 0)
            self.amountOfCompanies[company] += 1
            if currency != '':
                if currency != '₽':
                    self.valueofCompanyForeign.setdefault(company, [])
                    self.valueofCompanyForeign[company].extend([salary, currency])
                else:
                    self.valueofCompany.setdefault(company, [])
                    self.valueofCompany[company].append(salary)
        
        Parcer.loggerParcer.info('---------------------------------')
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
        Parcer.loggerParcer.info('Updating last vacancy.')
        for message in messages:
            self._update_last_vacancy(message)
            break

class Vacancies:

    def __init__(self):
        self.job = Parcer()
        self.mysql = Mysql()

    def _get_information(self) -> None:
        messages = self.job._get_dialogs()
        for message in messages:
            if message.text != lastVacancy:
                company, salary, stack = self.job._get_info(message)
                if (not stack) or (not salary): 
                    continue
                self.job.amountOfVacancions += 1
                correctStack = self.job._get_stack(stack)
                correctCompany = self.job._get_company(company)
                if salary != 'Вакансия без зарплаты':
                    correctSalary, correctCurrency = self.job._get_salary(salary)
                    self.job._get_value(correctStack, correctSalary, correctCurrency, correctCompany)
                else:
                    correctCurrency = ''
                    self.job._get_value(correctStack, salary, correctCurrency, correctCompany)
            else:
                self.job._get_last_vacancy(messages)
                break

    def _update_company_information(self) -> None:
        companiesListSalary = self.mysql._get_companies_for_salary()
        for key, value in self.job.valueofCompany.items():
            lenCompany = sum([salary != 'Вакансия без зарплаты' for salary in value])
            if lenCompany != 0:
                if key in companiesListSalary:
                    salaryValue = sum([int(salary) for salary in value]) / len(value)
                    averageTable = self.mysql._get_company_average_salary(key)
                    averageSalary = int((salaryValue + averageTable) / 2)
                    self.mysql._update_company_average_salary(key, averageSalary)
                else:
                    self.mysql._insert_into_company_average_salary(key, int(value[0]))
        for key, value in self.job.valueofCompanyForeign.items():
            if key in companiesListSalary:
                averageTable = self.mysql._get_company_average_salary(key)
                averageSalary = int((value[0] + averageTable) / 2)
                self.mysql._update_company_average_salary(key, averageSalary)
            else:
                self.mysql._insert_into_company_average_salary(key, int(value[0]), value[1])

    def _update_skills_list(self) -> None:
        skillsList = self.mysql._get_skills()
        for key, value in self.job.amountOfSkill.items():
            if key in skillsList:
                self.mysql._update_skills_amount(key, value)
            else:
                self.mysql._insert_into_skills_amount(key, value)

    def _update_companies_list(self) -> None:
        companiesList = self.mysql._get_companies()
        for key, value in self.job.amountOfCompanies.items():
            if key in companiesList:
                self.mysql._update_companies_amount(key, value)
            else:
                self.mysql._insert_into_companies_amount(key, value)
        self.mysql._update_vacancies_amount(self.job.amountOfVacancions)

    def _update_skills_value(self) -> None:
        for salary, stack in self.job.valueOfSalary.items():
            stack = list(set(stack))
            valueOfVacancy = sum([self.mysql._get_skill_amount(skill) for skill in stack])
            skillsList = self.mysql._get_skills_from_value()
            for skill in stack:
                amount = self.mysql._get_skill_amount(skill)
                valueVacancy = int(salary * amount / valueOfVacancy)
                if skill in skillsList:
                    valueTable = self.mysql._get_skill_value(skill)
                    valueOfSkill = int((valueVacancy + valueTable) / 2)
                    self.mysql._update_value_amount(skill, valueOfSkill)
                else:
                    self.mysql._insert_into_skills_value(skill, valueVacancy)
        if self.job.valueOfSalary != {}:
            averageSalVacancy = sum([salary for salary in self.job.valueOfSalary.keys()]) / len(self.job.valueOfSalary.keys())
            averageSalTable = self.mysql._get_average_salary()
            averageSalary = int((averageSalTable + averageSalVacancy) / 2)
            self.mysql._update_average_salary(averageSalary)
    

