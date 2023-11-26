# Define customer classes
import threading
import time
import random
import names

class Customer():
    def __init__(self, id, casino: object):
        self.customer_id = id
        # self.log_file = 'customers_log.txt'
        self.bankroll = None
        self.gender = random.choice("male", "female")
        self.name = names.get_full_name(gender=self.gender)
        self.age = random.randint(18,80)
        self.lock = threading.Lock()
        self.casino: object = casino

    def enter_bouncer_queue(self):
        try:
            for bouncer in self.casino.bouncers:
                if not bouncer['queue']:
                    with bouncer.bouncer['lock']:
                        bouncer.bouncer['queue'].append(self)
                        return bouncer
            else:
                bouncer = random.choice(self.casino.bouncers)
                with bouncer.bouncer['lock']:
                    bouncer.bouncer['queue'].append(self)
                    return bouncer
        except:
            return None
             
    @staticmethod
    def player_info(func):                # Will be changed to log into 'customers_log.txt'
        def print_id(self, amount):
            print(f'Player [{self.customer_id}] updated bankroll by: [{amount}]')
            return func(self, amount)
        return print_id
    
    @player_info 
    def update_bankroll(self, amount) -> float:        
        """
        Decorator prints depending on customer_id
        Updates a customers balance/bankroll
        """
        self.bankroll += amount
        return self.bankroll
    
    def get_bankroll(self):
        return self.bankroll

    def order_drink(self, options:list):
        drink = random.choice(options)
        return drink
        
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def goBathroom(self):
        time.sleep(random.randrange(1, 20))

    def run(self):   # NEEDS FINISHING
        while self.casino.is_open:
            current_bouncer = self.enter_bouncer_queue()
            #current_bouncer.
            self.casino.customers.append(self)


class HighRoller(Customer):
    def __init__(self, id):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(10000, 100000)


class MediumRoller(Customer):
    def __init__(self, id):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(1000, 10000)


class LowRoller(Customer):
    def __init__(self, id):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(100, 1000)


def customer_type(id, customer_type=None) -> HighRoller or MediumRoller or LowRoller:
    """
    Factory Method
    :params: high, medium, low
    """

    customer = {'high': HighRoller(id),
                'medium': MediumRoller(id),
                'low': LowRoller(id)}
    
    return customer[customer_type](id)