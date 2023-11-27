import random
import names
import threading

class Bartender():

    drinks = ['Mojito', 'Martini', 'Cosmopolitan', 'Beer', 'Wine', 'Whiskey', 'Tequila Sunrise', 'Gintonic']
    drink_price = 5

    def __init__(self, id, casino: object):
        self.bartender_id = id
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
        self.current_customer = None
        self.current_drink = None
        self.casino: object = casino

    def select_customer(self):
        with self.casino.locks['bartender']:
            if self.casino.queues['bartender']:
                self.current_customer = self.casino.queues['bartender'].pop()
                return self.current_customer
            return None

    def take_order(self, drink_options: list):
        self.current_drink = self.current_customer.order_drink(drink_options)
        return self.current_drink       
    
    def make_drink(self, drink):
        if self.current_drink:
            print(f"{self.name} makes a {drink}.")
            return drink
        else:
            print(f"{self.name} needs an order from a customer first.")

    def serve_drink(self, customer):
        if self.current_drink:
            print(f"{self.name} serves a {self.current_drink} to {customer.name}.")
        else:
            print(f"{self.name} needs an order from a customer first.")

    
    def run(self):
        while self.casino.is_open:
            self.current_customer = self.select_customer()
            if self.current_customer:
                self.current_drink = self.take_order(self.drinks)
                self.make_drink(self.current_drink)
                self.casino.update_balance(5, Bartender)

                self.current_customer = None
                self.current_drink = None
            else:
                continue

    


