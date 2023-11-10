# Casino class

import threading
import time
import random

class Casino:

    def __init__(self, starting_balance) -> None:
        self.balance = starting_balance
        self.tables = []
        self.customers = []
        self.employees = []
        self.opening_time = 0
        self.closing_time = 1000
        self.lock = threading.Lock()

    def get_balance(self):
         return self.balance
    
    def update_balance(self, amount):
         self.balance += amount
    
    def add_customer(self, customer):
            with self.lock:
                self.customers[customer.name] = customer

    def remove_customer(self, customer):
        with self.lock:
            del self.customers[customer.name]

    def run(self):
         print(f"The Casino is now open.")
         time.sleep(self.closing_time)
         print(f"casino is now closed.")


    