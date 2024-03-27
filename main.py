from parcer import Parcer
from mysql import Mysql

from last_vacancy import lastVacancy 
from loguru import logger

job = Parcer()

messages = job._get_dialogs()

for message in messages:
    if message.text != lastVacancy:
        salary, stack = job._get_info(message)
        if not stack or not salary: 
            continue
        job.amountOfVacancions += 1
        correctStack = job._get_stack(stack)
        if salary != 'Вакансия без зарплаты':
            correctSalary = job._get_salary(salary)
            job._get_value(correctStack, correctSalary)
        else:
            job._get_value(correctStack, salary)
    else:
        job._get_last_vacancy(messages)
        break


mysql = Mysql()

skills_list = mysql._get_skills()
for key, value in job.amountOfSkill.items():
    if key in skills_list:
        mysql._update_skills_amount(key, value)
    else:
        mysql._insert_into_skills_amount(key, value)
mysql._update_vacancies_amount(job.amountOfVacancions)


for salary, stack in job.valueOfSalary.items():
    stack = list(set(stack))
    valueOfVacancy = sum([mysql._get_skill_amount(skill) for skill in stack])
    skillsList = mysql._get_skills_from_value()
    for skill in stack:
        amount = mysql._get_skill_amount(skill)
        valueVacancy = int(salary * amount / valueOfVacancy)
        if skill in skillsList:
            valueTable = mysql._get_skill_value(skill)
            valueOfSkill = int((valueVacancy + valueTable) / 2)
            mysql._update_value_amount(skill, valueOfSkill)
        else:
            mysql._insert_into_skills_value(skill, valueVacancy)
if job.valueOfSalary != {}:
    averageSalVacancy = sum([salary for salary in job.valueOfSalary.keys()]) / len(job.valueOfSalary.keys())
    averageSalTable = mysql._get_average_salary()
    averageSalary = int((averageSalTable + averageSalVacancy) / 2)
    mysql._update_average_salary(averageSalary)




