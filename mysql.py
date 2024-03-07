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

    def _insert_into_skills_amount(self, skill: str, amount: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO skills_amount (skill, amount) VALUES ('{skill}', {amount});"
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
    
    def _update_vacancies_amount(self, amount:int) -> None:
        try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE vacancies_amount SET amount = amount + {amount};"
                cursor.execute(update_table_query)
                self.connection.commit()
        except Exception as ex:
            print("Mistake while updating amount of vacancies...")
