# Define customer classes
import threading
import time
import random
import names

class Customer():
    def __init__(self, id, casino: object):
        self.customer_id = id
        self.in_casino = False
        self.bankroll = None
        self.gender = random.choice('male', 'female')
        self.name = names.get_full_name(gender=self.gender)
        self.age = random.randint(18,80)
        self.casino: object = casino

    def enter_bouncer_queue(self):
        try:
            with self.casino.lock['bouncer']:
                self.casino.queues['bouncer']
            return True
        except:
            return False
        
    def check_status(self):
        if self in self.casino.customers:
            self.in_casino = True
            return True
        elif self in self.casino.customers_denied_entry:
            return False
        else:
            return False

             
    @staticmethod
    def player_info(func):                # Will be changed to logged into SQL
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
        self.enter_bouncer_queue()
        if self.check_status(self) is True:
            while self.casino.is_open:
                activity = random.choice(['play', 'drink', 'bathroom', 'observe'], weights=[0.6, 0.3, 0.05, 0.05], k=1)

                if activity.lower() == 'play':
                    self.casino.queues['table']['customer'].append(self)
                elif activity.lower() == 'drink':
                    self.casino.queues['bartender'].append(self)
                elif activity.lower() == 'bathroom':
                    self.casino.bathrooms[self.gender].append(self)
                    self.goBathroom()
                else:
                    time.sleep(random.randrange(5,10))

                         
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