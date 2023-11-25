import random
import names
import threading
import concurrent.futures
from casino_class import Casino

class Bartender():
    def __init__(self, id):
        super().__init__()
        self.bartender_id = id
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
        self.drinks = ["Mojito", "Martini", "Cosmopolitan", "Beer", "Wine", "Whiskey", "Tequila Sunrise", "Gintonic"]
        self.current_customer = None
        self.current_drink = None
        self.customer = {'lock': threading.Lock(), 'queue': []}
        self.casino = Casino()

    def customer_waiting(self):
        with self.customer['lock']:
            if self.customer['queue']:
                return True
            return False
    
    def select_customer(self):
        with self.customer['lock']:
            self.current_customer = self.customer['queue'].pop()
            return self.current_customer

    def take_order(self):
        self.current_drink = self.current_customer.order_drink(self.drinks)    # MUST APPLY TO CUSTOMER CLASS
        return self.current_drink       
    
    def make_drink(self):
        if self.current_drink:
            print(f"{self.name} makes a {self.current_drink}.")
            return self.current_drink
        else:
            print(f"{self.name} needs an order from a customer first.")

    def serve_drink(self, customer):
        if self.current_drink:
            print(f"{self.name} serves a {self.current_drink} to {customer.name}.")
        else:
            print(f"{self.name} needs an order from a customer first.")

    def run(self):
        while self.casino.is_open:
            if self.orders:


