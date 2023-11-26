import random
import names
import threading

class Bartender():

    drinks = ['Mojito', 'Martini', 'Cosmopolitan', 'Beer', 'Wine', 'Whiskey', 'Tequila Sunrise', 'Gintonic']
    
    def __init__(self, id, casino: object):
        self.bartender_id = id
        # self.log_file = 'bartenders_log.txt'
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
        self.current_customer = None
        self.current_drink = None
        self.customer = {'lock': threading.Lock(), 'queue': []}
        self.casino: object = casino

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
        self.current_drink = self.current_customer.order_drink(self.drinks)
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
            pass

    


