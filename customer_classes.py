import time
import random
import names

class Customer():
    def __init__(self, id=None, casino=None):
        self.customer_id = id
        self.in_casino = False
        self.bankroll = None
        self.gender = random.choice(['male', 'female'])
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

    def update_customers(self, values:tuple, table='customers'):
        with self.casino.locks['db']:
            self.casino.database.insert_table(table, values)


    def run(self):   # NEEDS FINISHING
        try:
            self.enter_bouncer_queue()
            if self.check_status(self) is True:
                self.update_customers(self, values=tuple(self.customer_id, name=self.name, age=self.age, gender=self.gender))
                while self.casino.is_open:
                    activity = random.choice(['play', 'drink', 'bathroom', 'observe'], weights=[0.6, 0.3, 0.05, 0.05], k=1)[0]

                    if activity.lower() == 'play':
                        self.casino.queues['table']['customer'].append(self)
                    elif activity.lower() == 'drink':
                        self.casino.queues['bartender'].append(self)
                    elif activity.lower() == 'bathroom':
                        self.casino.bathrooms[self.gender].append(self)
                        self.goBathroom()
                    else:
                        time.sleep(random.randrange(5,10))
        except:
            print("Error in customer")

                         
class HighRoller(Customer):
    def __init__(self, id, casino:object):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(10000, 100000)
        self.casino:object = casino


class MediumRoller(Customer):
    def __init__(self, id, casino:object):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(1000, 10000)
        self.casino:object = casino


class LowRoller(Customer):
    def __init__(self, id, casino:object):
        super().__init__(self)
        self.customer_id = id
        self.bankroll = random.randint(100, 1000)
        self.casino:object = casino


def customer_type(id, casino:object, type=None):
    """
    Factory Method
    :params: high, medium, low
    """

    customer = {'high': HighRoller(id, casino),
                'medium': MediumRoller(id, casino),
                'low': LowRoller(id, casino)}
    
    return customer[type]()