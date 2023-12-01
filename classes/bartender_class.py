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
                self.casino.LOG.info(f"Selected customer {self.current_customer}")
                return self.current_customer
            return None

    def take_order(self, drink_options: list):
        self.current_drink = self.current_customer.order_drink(drink_options)
        return self.current_drink       
    
    def make_drink(self, drink):
        if self.current_drink:
            return drink
        else:
            pass

    def serve_drink(self, customer):
        if self.current_drink:
            pass
        else:
            pass

    
    def run(self):
        try:
            self.casino.LOG.info(f"Created bartender {self.bartender_id} thread")
            while self.casino.is_open:
                self.current_customer = self.select_customer()
                if self.current_customer:
                    self.casino.LOG.info(f"Bartender selected customer {self.current_customer}")
                    self.current_drink = self.take_order(self.drinks)
                    self.make_drink(self.current_drink)
                    self.casino.update_balance(5, executor=Bartender)

                    self.current_customer = None
                    self.current_drink = None
                else:
                    continue
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)

    


