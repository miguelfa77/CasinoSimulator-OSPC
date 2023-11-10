import random
import names
import concurrent.futures

class Bartender:
    def __init__(self):
        self.Name = names.get_first_name()
        self.Age = random.randint(18, 60)
        self.drinks = ["Mojito", "Martini", "Cosmopolitan", "Beer", "Wine", "Whiskey", "Tequila Sunrise", "Gintonic"]
        self.current_drink = None

    def take_order(self, customer):
        self.current_drink = random.choice(self.drinks)
        print(f"{self.name} takes an order from {customer.name} for a {self.current_drink}.")

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

class Customer:
    def __init__(self, bartender):
        self.name = names.get_first_name()
        self.bartender = bartender

    def run(self):
        self.bartender.take_order(self)
        drink = self.bartender.make_drink()
        self.bartender.serve_drink(self)
        print(f"{self.name} enjoys the {drink}.")

bartender = Bartender()
customers = [Customer(bartender) for _ in range(15)]

with concurrent.futures.ThreadPoolExecutor() as executor:
    for customer in customers:
        executor.submit(customer.run)



