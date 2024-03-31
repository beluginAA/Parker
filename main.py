from parcer import Parcer
from mysql import Mysql

from last_vacancy import lastVacancy 
from loguru import logger

job = Parcer()

messages = job._get_dialogs()
iter = 0
for message in messages:
    iter += 1
    if iter == 10:
        break
    if message != lastVacancy:
        company, salary, stack = job._get_info(message)
        if not stack or not salary: 
            continue
        job.amountOfVacancions += 1
        correctStack = job._get_stack(stack)
        correctCompany = job._get_company(company)
        if salary != 'Вакансия без зарплаты':
            correctSalary = job._get_salary(salary)
            job._get_value(correctStack, correctSalary, correctCompany)
        else:
            job._get_value(correctStack, salary, correctCompany)
    else:
        job._get_last_vacancy(messages)
        break


mysql = Mysql()

companiesListSalary = mysql._get_companies_for_salary()
for key, value in job.valueofCompany.items():
    lenCompany = sum([salary != 'Вакансия без зарплаты' for salary in value])
    if lenCompany != 0:
        if key in companiesListSalary:
            salaryValue = sum([int(salary) for salary in value]) / len(value)
            averageTable = mysql._get_company_average_salary(key)
            averageSalary = int((salaryValue + averageTable) / 2)
            mysql._update_company_average_salary(key, averageSalary)
        else:
            mysql._insert_into_company_average_salary(key, int(value[0]))

skillsList = mysql._get_skills()
for key, value in job.amountOfSkill.items():
    if key in skillsList:
        mysql._update_skills_amount(key, value)
    else:
        mysql._insert_into_skills_amount(key, value)

companiesList = mysql._get_companies()
for key, value in job.amountOfCompanies.items():
    if key in skillsList:
        mysql._update_companies_amount(key, value)
    else:
        mysql._insert_into_companies_amount(key, value)

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