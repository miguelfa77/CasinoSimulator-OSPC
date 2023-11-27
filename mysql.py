import os
import mysql.connector

def get_mysql_credentials():

    password = os.environ.get('MYSQL_PASSWORD')

    return password

def mysql_connect(db=None):
   """
   Connect to mySQL
   :params db: Optional parameter for database name
   :return: mySQL connection object
   """

   password = get_mysql_credentials()
   
   if db is not None:
        conn = mysql.connector.connect(host='localhost',
                        user='root',
                        password=password,
                        database=db)
        return conn

   else:
    conn = mysql.connector.connect(host='localhost',
                        user='root',
                        password=password)
   
    return conn
   
conn = mysql_connect()
print(conn)




