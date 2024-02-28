import pymysql

from config import host, port, user, password, database

class Mysql:
    
    def __init__(self):
        try:
            self.connection = pymysql.connect(host, port, user, password,
            database, cursorclass=pymysql.cursors.DictCursor)
        except Exception as ex:
            print("Connection refused...")
    
    def insert(self) -> None:
        try:
            with self.connection.cursor() as cursor:
                # create_table_query = "CREATE TABLE `users`(id int AUTO_INCREMENT," \
                #             " name varchar(32)," \
                #             " password varchar(32)," \
                #             " email varchar(32), PRIMARY KEY (id));"
                # cursor.execute(create_table_query)
                print("Table created successfully")
        finally:
            self.connection.close() 


mysql = Mysql()
mysql