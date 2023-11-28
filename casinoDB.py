import os
import mysql.connector
import logging
from typing import Literal

class DB:
    def __init__(self):
        self.db = None
        self.tables = []
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
                print('Worked db')
            else:
                self.conn = mysql.connector.connect(**self.config)
                print('Worked no db')

            
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
        
    def create_db(self, db=None):
        try:
            if self.auth():
                self.db = db
                self.conn.cursor().execute(
                    "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.db)
                )
                self.kill_conn()
                print(f"Successfully created database {self.db}")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)
    
    def create_table(self, table):
        """
        :params: table ['transactions' or 'customers']
        """
        self.auth()
        query = {
            'transactions': """CREATE TABLE IF NOT EXISTS transactions(
                            transaction_id INT PRIMARY KEY AUTO_INCREMENT,
                            executor VARCHAR (255) NOT NULL,
                            amount INT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL);
                            """,   
            'customers': """CREATE TABLE customers(
                            customer_id INT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            age VARCHAR(255) NOT NULL,
                            gender VARCHAR(255));
                            """    
        }
        
        if table.lower() in ['transactions', 'customers']:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query[table])
                self.conn.commit()
                return True

            except (mysql.connector.Error, IOError) as err:
                self.conn.rollback()
                print(f"Something went wrong: {err}")
                return None      
        else:
            raise ValueError("Invalid table name. Please use 'transactions'")



        

pool = DB()
pool.create_db('casino')
pool.create_table('transactions')
pool.kill_conn()

        
    




