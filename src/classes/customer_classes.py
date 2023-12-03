import time
import random
import names

class Customer():
    def __init__(self, id=None, casino=None):
        self.id = id
        self.in_casino = False
        self.bankroll = None
        self.gender = random.choice(['male', 'female'])
        self.name = names.get_full_name(gender=self.gender)
        self.age = random.randint(18,80)
        self.current_table = None
        self.served = False
        self.customer_type = "normal"
        self.entry_atts_ = {"drunkness":random.randint(0,8),
                            "rage":random.randint(0,8),
                            "is_vip": random.choices([True,False], weights=(10,90), k=1)[0],
                            "has_weapon": random.choices([True,False], weights=(5,95), k=1)[0]} 
        self.min_bet_amount = 1
        self.casino: object = casino

    def enter_bouncer_queue(self):
        try:
            with self.casino.locks['bouncer']:
                self.casino.queues['bouncer'].append(self)
                return True
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)
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
    def player_info(func):
        def print_id(self, amount):
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

    def bet(self, amount): 
        while amount < self.min_bet_amount:
            if amount < self.min_bet_amount:
                amount *= 3
        self.update_bankroll(amount)
        return amount
    
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def order_drink(self, drinks):
        choice = random.choice(drinks)
        return choice
         
    def goBathroom(self):
        if len(self.casino.queues['bathroom'][self.gender]) < 5:
            with self.casino.locks['bathroom'][self.gender]:
                self.casino.queues['bathroom'][self.gender].append(self)
            time.sleep(random.randrange(1, 20))
            with self.casino.locks['bathroom'][self.gender]:
                self.casino.queues['bathroom'][self.gender].remove(self)
        else:
            pass

    def update_customers(self, values:tuple, table='customers'):
        with self.casino.locks['db']:
            self.casino.database.insert_table(table, values)
    
    def enter_bartender_queue(self):
        with self.casino.locks['bartender']:
            self.casino.queues['bartender'].append(self)

    def leave_bartender(self):
        while not self.served and self.casino.is_open:
            pass
        if self.served:
            with self.casino.locks['bartender']:
                self.served = False

    def enter_table_queue(self):
        with self.casino.locks['table']['customer']:
            self.casino.queues['table']['customer'].append(self)

    def leave_table(self):
        with self.casino.locks['table']['customer']:
            if self.current_table:
                self.current_table.current_customers.remove(self)
                self.current_table = None
            

    def run(self):
        self.casino.LOG.info(f"Running customer [{self.id}] thread")
        try:
            self.enter_bouncer_queue()
            self.casino.LOG.info(f"Customer [{self.id}] entered bouncer queue")
            while self not in self.casino.customers_denied_entry and self not in self.casino.customers and self.casino.is_open:
                time.sleep(1)
            if self.check_status() is True:
                self.update_customers(values=tuple([self.id, self.name, self.age, self.gender]))
                while self.casino.is_open:
                    activity = random.choices(['play', 'drink', 'bathroom', 'observe'], weights=[0.75, 0.15, 0.05, 0.05], k=1)[0]

                    if activity.lower() == 'play':
                        self.enter_table_queue()
                        time.sleep(60)
                        self.leave_table()
                        self.casino.LOG.debug(f"Customer [{self.id}]: left table")

                    elif activity.lower() == 'drink':
                        self.enter_bartender_queue()
                        time.sleep(10)
                        self.leave_bartender()
                        self.casino.LOG.debug(f"Customer [{self.id}]: ordered drink")

                    elif activity.lower() == 'bathroom':
                        self.goBathroom()
                        self.casino.LOG.debug(f"Customer [{self.id}]: went to bathroom")
                    else:
                        time.sleep(random.randrange(2,5))
                self.casino.LOG.info(f"Customer [{self.id}]: Thread finished")
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)   


class HighRoller(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.bankroll = random.randint(5000000, 9999999)
        self.start_bankroll = self.bankroll
        self.min_bet_amount = 100000
        self.customer_type = "high_roller"

    def enterVIP(self):
        print(f"Customer {self.name} has entered the VIP.")
        time.sleep(random.randint(5,20))
        print(f"Customer {self.name} has left the VIP.")


class MediumRoller(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.bankroll = random.randint(100000,999999)
        self.start_bankroll = self.bankroll
        self.min_bet_amount = 10000
        self.customer_type = "medium_roller"


class LowRoller(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.bankroll = random.randint(10000,99999)
        self.start_bankroll = self.bankroll
        self.min_bet_amount = 1000
        self.customer_type = "low_roller"

def customer_type(id, casino:object, type=None):
    """
    Factory Method
    :params: high, medium, low
    """

    customer = {'high': HighRoller,
                'medium': MediumRoller,
                'low': LowRoller}
    
    return customer[type](id, casino)

