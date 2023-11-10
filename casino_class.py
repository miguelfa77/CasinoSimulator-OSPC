# Casino class

import threading
import time
import random

class Casino:
    def __init__(self) -> None:
        self.tables = []
        self.customers = []
        self.employees = []
        self.bathrooms = {"Mens": [],
                          "Womens": []}
        self.opening_time = 0
        self.closing_time = 1000
        self.lock = threading.Lock()

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


    