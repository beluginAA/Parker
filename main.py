from parcer import Parcer
from mysql import Mysql

from last_vacancy import lastVacancy 

job = Parcer()

messages = job._get_dialogs()

for message in messages:
    if message.text != lastVacancy:
        salary, stack = job._get_info(message)
        if not stack or not salary: 
            continue
        job.amountOfVacancions += 1
        correctSalary = job._get_salary(salary)
        correctStack = job._get_stack(stack)
        job._get_value(correctStack, correctSalary)
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




