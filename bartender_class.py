import random
import names
import threading

class Bartender():
    def __init__(self, id, casino):
        self.casino = casino
        self.bartender_id = id
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
        self.drinks = ["Mojito", "Martini", "Cosmopolitan", "Beer", "Wine", "Whiskey", "Tequila Sunrise", "Gintonic"]
        self.current_drink = None
        self.lock = threading.Lock()
        self.casino.bartenders.append(self)

    def take_order(self, customer):
        with self.lock:
            self.current_drink = random.choice(self.drinks)
            print(f"{self.name} takes an order from {customer.name} for a {self.current_drink}.")

    def make_drink(self):
        with self.lock:
            if self.current_drink:
                print(f"{self.name} makes a {self.current_drink}.")
                return self.current_drink
            else:
                print(f"{self.name} needs an order from a customer first.")

    def serve_drink(self, customer):
        with self.lock:
            if self.current_drink:
                print(f"{self.name} serves a {self.current_drink} to {customer.name}.")
            else:
                print(f"{self.name} needs an order from a customer first.")
