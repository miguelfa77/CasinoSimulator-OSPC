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
                self.current_customer = self.casino.queues['bartender'].pop(0)

    def take_order(self, drink_options):
        with self.casino.locks['bartender']:
            self.current_drink = self.current_customer.order_drink(self, drink_options)
            self.casino.update_balance(5, executor=Bartender.__name__)
            self.current_customer.served = True     
    
    def run(self):
        self.casino.LOG.info(f"Running bartender [{self.bartender_id}] thread")
        try:
            while self.casino.is_open:
                self.select_customer(self)
                if self.current_customer:
                    self.take_order(self, drink_options=self.drinks)
                    if self.current_customer and self.current_drink:
                        self.current_customer = None
                        self.current_drink = None
                else:
                    continue
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)

    


