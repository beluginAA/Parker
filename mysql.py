import pymysql

from config import host, port, user, password, database

class Mysql:
    
    def __init__(self):
        try:
            self.connection = pymysql.connect(host=host, port=port, 
            user=user, password=password, 
            database=database, cursorclass=pymysql.cursors.DictCursor)
        except Exception as ex:
            print("Connection refused...")
    
    def _get_vacancies_amount(self) -> int:
        try:
            with self.connection.cursor() as cursor:
                get_vacancies_query = "SELECT amount FROM vacancies_amount;"
                cursor.execute(get_vacancies_query)
                
                row = cursor.fetchall()
            return row[0]['amount']
        except Exception as ex:
            print("Mistake while getting vacansies amount...")
    
    def _get_average_salary(self) -> int:
        try:
            with self.connection.cursor() as cursor:
                get_salary_query = "SELECT average_salary FROM average_salary;"
                cursor.execute(get_salary_query)
                
                row = cursor.fetchall()
            return row[0]['average_salary']
        except Exception as ex:
            print("Mistake while getting average salary...")

    def _get_skills(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill FROM skills_amount;"
                cursor.execute(get_skills_query)
                
                rows = cursor.fetchall()
                skills_list = [row['skill'] for row in rows]
            return skills_list
        except Exception as ex:
            print("Mistake while getting skills...")
    
    def _get_companies(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_companies_query = "SELECT company FROM companies_amount;"
                cursor.execute(get_companies_query)
                
                rows = cursor.fetchall()
                company_list = [row['company'] for row in rows]
            return company_list
        except Exception as ex:
            print("Mistake while getting companies...")

    def _get_companies_for_salary(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_companies_query = "SELECT company FROM companies_average_salary;"
                cursor.execute(get_companies_query)
                
                rows = cursor.fetchall()
                company_list = [row['company'] for row in rows]
            return company_list
        except Exception as ex:
            print("Mistake while getting companies for average salary...")
    
    def _get_skills_from_value(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill FROM skills_value;"
                cursor.execute(get_skills_query)
                
                rows = cursor.fetchall()
                skills_list = [row['skill'] for row in rows]
            return skills_list
        except Exception as ex:
            print("Mistake while getting skills...")
    
    def _get_skill_value(self, skill:str) -> int:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"SELECT value FROM skills_value WHERE skill = '{skill}';"
                cursor.execute(update_table_query)

                rows = cursor.fetchall()
                skill_amount = rows[0]['value']
                self.connection.commit()
                return skill_amount
        except Exception as ex:
            print("Mistake while gitting skill's amount...")

    def _get_skills_with_letters(self) -> dict[str:list[str]]:
        try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill FROM skills_amount;"
                cursor.execute(get_skills_query)
                
                rows = cursor.fetchall()
                skills_list, word_dict = [row['skill'] for row in rows], {}
                for word in skills_list:
                    first_letter = word[0] 
                    word_dict.setdefault(first_letter, []).append(word)
                sorted_word_dict = dict(sorted(word_dict.items()))
            return sorted_word_dict
        except Exception as ex:
            print("Mistake while getting skills with letters...")

    def _get_most_popular_skills(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill, amount FROM skills_amount ORDER BY amount DESC LIMIT 10;"
                cursor.execute(get_skills_query)
                
                rows, popular_skills_list = cursor.fetchall(), []
                for row in rows:
                    popular_skills_list.append(f'{row["skill"]} - {row["amount"]}\n')
            return popular_skills_list
        except Exception as ex:
            print("Mistake while getting the most popular skills...")
    
    def _get_less_popular_skills(self) -> list[str]:
        try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill, amount FROM skills_amount ORDER BY amount LIMIT 10;"
                cursor.execute(get_skills_query)
                
                rows, nonpopular_skills_list = cursor.fetchall(), []
                for row in rows:
                    nonpopular_skills_list.append(f'{row["skill"]} - {row["amount"]}\n')
            return nonpopular_skills_list
        except Exception as ex:
            print("Mistake while getting the less popular skills...")
    
    def _get_skill_amount(self, skill:str) -> int:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"SELECT amount FROM skills_amount WHERE skill = '{skill}';"
                cursor.execute(update_table_query)

                rows = cursor.fetchall()
                skill_amount = rows[0]['amount']
                self.connection.commit()
                return skill_amount
        except Exception as ex:
            print("Mistake while gitting skill's amount...")
    
    def _get_company_average_salary(self, company:str) -> int:
        try:
            with self.connection.cursor() as cursor:
                get_table_query = f"SELECT average_salary FROM companies_average_salary WHERE company = '{company}';"
                cursor.execute(get_table_query)

                rows = cursor.fetchall()
                average_salary = rows[0]['average_salary']
                self.connection.commit()
                return average_salary
        except Exception as ex:
            print("Mistake while gitting companie's average salary...")

    def _insert_into_skills_amount(self, skill: str, amount: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO skills_amount (skill, amount) VALUES ('{skill}', {amount});"
                cursor.execute(insert_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while inserting into skill's amount...")
    
    def _insert_into_company_average_salary(self, company: str, salary: int, currency = '₽') -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO companies_average_salary (company, average_salary, currency) VALUES ('{company}', {salary}, '{currency}');"
                cursor.execute(insert_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while inserting into companie's average salary...")
    
    def _insert_into_companies_amount(self, company: str, amount: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO companies_amount (company, amount) VALUES ('{company}', {amount});"
                cursor.execute(insert_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while inserting into companie's amount...")
    
    def _insert_into_skills_value(self, skill: str, amount: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO skills_value (skill, value) VALUES ('{skill}', {amount});"
                cursor.execute(insert_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while inserting into skill's amount...")
    
    def _update_skills_amount(self, skill:str, value: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE skills_amount SET amount = amount + {value} WHERE skill = '{skill}';"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating skill's amount...")
    
    def _update_company_average_salary(self, company:str, value: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE companies_average_salary SET average_salary = {value} WHERE company = '{company}';"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating skill's amount...")
    
    def _update_companies_amount(self, company:str, value: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE companies_amount SET amount = amount + {value} WHERE company = '{company}';"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating companie's amount...")
    
    def _update_value_amount(self, skill:str, value: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE skills_value SET value = {value} WHERE skill = '{skill}';"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating skill's value...")
    
    def _update_vacancies_amount(self, amount:int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE vacancies_amount SET amount = amount + {amount};"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating amount of vacancies...")
    
    def _update_average_salary(self, amount:int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE average_salary SET average_salary = {amount};"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating average salary...")
