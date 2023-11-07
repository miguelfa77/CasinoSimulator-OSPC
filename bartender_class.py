import random
import names

class Bartender:
    def __init__(self):
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
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
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    bartender = Bartender("John")
    customer = Customer("Alice")

    bartender.take_order(customer)
    bartender.make_drink()
    bartender.serve_drink(customer)

