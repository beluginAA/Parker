import pymysql

class Mysql:
    
    def __init__(self):
        try:
            connection = pymysql.connect(
            host='127.0.0.1',
            port=33061,
            user='us',
            password='User123!',
            database='parcer_info',
            cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)
        except Exception as ex:
            print("Connection refused...")
            print(ex)

mysql = Mysql()
mysql