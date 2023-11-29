import os
import mysql.connector
import logging
from typing import Literal

class casinoDB():
    def __init__(self):
        self.db = None
        self.tables = []
        self.config = {'user':'root',
                       'password':os.environ.get('MYSQL_PASSWORD'),
                       'host':'localhost',
                       'port':'3306'}
        self.conn = None
        self.initialize_db()

    def initialize_db(self):
        """
        Drop and recreate DB in case program has already ran.
        Create both tables
        """
        self.drop_db('casino')
        self.create_db('casino')

        self.create_table('customers')
        self.create_table('transactions')
    
    def drop_db(self, db=None):
        try:
            with self.auth():
                self.db = db
                cursor = self.conn.cursor()
                query = f"""DROP DATABASE IF EXISTS {self.db};"""
                cursor.execute(query)
                self.conn.commit()

        finally:
            self.kill_conn()
    
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
            self.conn = mysql.connector.connect(database=self.db, **self.config)
            print('Worked db')
            return self.conn

        except:
            self.conn = mysql.connector.connect(**self.config)
            print('Worked no db')
            return self.conn
    
    def kill_conn(self):
        if self.conn.is_connected():
            self.conn.close()
            print("Connection killed successfully")
            return True
        else:
            print("Connection failed to kill")
            return False
          
    def __enter__(self):
        return self.auth()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill_conn() 
        
    def create_db(self, db=None):
        try:
            with self.auth():
                self.db = db
                cursor = self.conn.cursor()
                query =  f"""CREATE DATABASE IF NOT EXISTS {self.db} DEFAULT CHARACTER SET 'utf8'"""
                cursor.execute(query)
                self.conn.commit()
                self.kill_conn()
                print(f"Successfully created database {self.db}")

        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)
    
    def create_table(self, table):
        """
        :params: table ['transactions' or 'customers']
        """
        query = {
            'transactions': """CREATE TABLE IF NOT EXISTS transactions(
                            transaction_id INT PRIMARY KEY AUTO_INCREMENT,
                            executor VARCHAR (255) NOT NULL,
                            amount INT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL);
                            """,  
            'customers': """CREATE TABLE IF NOT EXISTS customers(
                            customer_id INT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL, 
                            age VARCHAR(255) NOT NULL,
                            gender VARCHAR(255));
                            """
        }   
        if table.lower() in ['transactions', 'customers']:
            try:
                with self.auth():
                    cursor = self.conn.cursor()
                    cursor.execute(query[table])
                    self.conn.commit()
                print(f"Successfully created table {table}")

            except (mysql.connector.Error, IOError) as err:
                print(f"Something went wrong: {err}")
                self.conn.rollback()
                return None      
        else:
            raise ValueError("Invalid table name. Please use 'transactions'")
        
    def insert_table(self, table, values:tuple):
        """
        :params: 
        - table: 'transactions' or 'customers'
        - values: 2 (executor, amount) or 4 (customer_id, name, age, gender)
        """
        query = {
            'transactions': """INSERT INTO transactions(executor, amount) VALUES (%s, %s);""" ,  
            'customers': """INSERT INTO customers(customer_id, name, age, gender) VALUES (%s, %s, %s, %s);"""
        }
        try:
            with self.auth():
                cursor = self.conn.cursor()
                cursor.execute(query[table], values)
                self.conn.commit()
                print(f"Successfully inserted into table {table}")

        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
        
"""
db = DB()

db.insert_table('transactions',('Table', 10))
db.insert_table('customers', (5, 'juan', 10, 'male'))

"""

        
    




