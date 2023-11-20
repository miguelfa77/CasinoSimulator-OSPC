# Casino class

import threading
import time
import random

class Casino:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Casino, cls).__new__(cls)
        return cls._instance

    def __init__(self, starting_balance, customers, tables, dealers, bartenders, bouncers) -> None:
        self.balance = starting_balance
        self.customers = customers
        self.tables = tables
        self.dealers = dealers
        self.bartenders = bartenders
        self.bouncers = bouncers
        self.bathrooms = {"Mens": [],
                          "Womens": [],
                          "mens_wc_lock": threading.Lock(),
                          "womens_wc_lock": threading.Lock()}
        self.opening_time = 0
        self.closing_time = 1000
        self.locks = {'customers_lock': threading.Lock(),
                      'dealers_lock': threading.Lock(),
                      'tables_lock': threading.Lock(),
                      'bartneders_lock': threading.Lock(),
                      'balance_lock': threading.Lock()}
        self.is_open = True

    def get_balance(self):
        return self.balance
    
    def update_balance(self, amount):
        with self.lock['balance_lock']:
            self.balance += amount
    
    def add_customer(self, customer):
        with self.lock['customer_lock']:
            self.customers[customer.name] = customer

    def remove_customer(self, customer):
        with self.lock['customer_lock']:
            del self.customers[customer.name]

    def run(self):
         print(f"The Casino is now open.")
         time.sleep(self.closing_time)
         self.is_open = False
         print(f"casino is now closed.")

         num_tables = random.randint(3,5)


    