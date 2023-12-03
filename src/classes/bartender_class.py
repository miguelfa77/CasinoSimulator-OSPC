import random
import names

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
        self.casino.update_balance(5, executor=Bartender.__name__)
        self.current_customer.served = True
        return self.current_drink      
    
    def run(self):
        self.casino.LOG.info(f"Running bartender [{self.bartender_id}] thread")
        try:
            while self.casino.is_open:
                self.current_customer = self.select_customer()
                if self.current_customer:
                    self.casino.LOG.info(f"Bartender selected customer [{self.current_customer.id}]")
                    self.current_drink = self.take_order(drink_options=self.drinks)
                    self.casino.LOG.debug(f"Bartender released customer [{self.current_customer.id}]")

                    if self.current_customer and self.current_drink:
                        self.current_customer = False
                        self.current_drink = False
                else:
                    continue
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)

    


