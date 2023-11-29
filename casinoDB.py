import os
import mysql.connector
import logging

class DB:
    def __init__(self):
        self.db = None
        self.config = {'user':'root',
                       'password':os.environ.get('MYSQL_PASSWORD'),
                       'host':'localhost',
                       'port':'3306'}
        self.conn = None
    
    def logger(self):
        """
        Print into terminal to monitor
        """

    
    def auth(self):
        """
        Connect to mySQL
        :params db: Optional parameter for db name
        :return: mySQL connection object
        """
        try:
            if self.db:
                self.conn = mysql.connector.connect(database=self.db, **self.config)
                print('Worked')
            else:
                self.conn = mysql.connector.connect(**self.config)
                print('Worked')
            
            return True

        except (mysql.connector.Error, IOError) as err:
            print(f"Something went wrong: {err}")
            return None
    
    def kill_conn(self):
        if self.conn.is_connected():
            self.conn.close()
            print("Connection killed successfully")
            return True
        else:
            print("Connection failed to kill")
            return False
        
    def query():
        pass
        

pool = DB()
pool.auth()
pool.kill_conn()

        
    




