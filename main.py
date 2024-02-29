from parcer import Parcer
from mysql import Mysql

from config import lastVacancy 

job = Parcer()

messages = job._get_dialogs()

for message in messages:
    if message != lastVacancy:
        salary, stack = job._get_info(message)
        if not stack or not salary: 
            continue
        correctSalary = job._get_salary(salary)
        correctStack = job._get_stack(stack)
        job._get_value(correctStack, correctSalary)
        break
    else:
        job._get_last_vacancy(messages)

mysql = Mysql()

for key, value in job.amountOfSkill.items():
    skills_list = mysql._get_skills()
    if key in skills_list:
        mysql._update(key, value)
    else:
        mysql._insert_into_skills_amount(key, value)




