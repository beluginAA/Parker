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
    
    def _get_skills(self) -> list[str]:
        # try:
            with self.connection.cursor() as cursor:
                get_skills_query = "SELECT skill FROM skills_amount;"
                cursor.execute(get_skills_query)
                
                rows = cursor.fetchall()
                skills_list = [row['skill'] for row in rows]
        # finally:
        #     self.connection.close() 
            return skills_list

    # def _insert_into_skills(self, skill: str) -> None:
    #     try:
    #         with self.connection.cursor() as cursor:
    #             insert_table_query = f"INSERT INTO `skills` (skill) VALUES ('{skill}')"
    #             cursor.execute(insert_table_query)
    #     finally:
    #         self.connection.close()

    def _insert_into_skills_amount(self, skill: str, amount: int) -> None:
        # try:
            with self.connection.cursor() as cursor:
                insert_table_query = f"INSERT INTO skills_amount (skill, amount) VALUES ('{skill}', {amount});"
                cursor.execute(insert_table_query)
                self.connection.commit()
        # finally:
            # self.connection.close()
    
    def _update(self, skill:str, value: int) -> None:
        # try:
            with self.connection.cursor() as cursor:
                update_table_query = f"UPDATE skills_amount SET amount = amount + {value} WHERE skill = '{skill}';"
                cursor.execute(update_table_query)
                self.connection.commit()
        # finally:
            # self.connection.close() 

# mysql = Mysql()