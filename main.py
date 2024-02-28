from parcer import Job
from mysql import Mysql

from config import lastVacancy 

vacancy = Job()

dialogs = vacancy.client.get_dialogs() 
for dialog in dialogs:
    if dialog.title == 'getmatch: бот с IT-вакансиями':
        messages = vacancy.client.iter_messages(dialog)
        break

for message in messages:
    if message != lastVacancy:
        print(message.text)
        salary, stack = vacancy._get_vacancy(message)
        if not stack: continue
        correctSalary = vacancy._get_salary(salary)
        correctStack = vacancy._get_stack(stack)
        vacancy._get_value(correctStack, correctSalary)
        break
    else:
        for message in messages:
            vacancy._update_last_vacancy(message)
            break


# mysql = Mysql()