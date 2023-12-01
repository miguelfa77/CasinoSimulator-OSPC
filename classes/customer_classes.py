import time
import random
import names
import threading

class Customer():
    def __init__(self, id=None, casino=None):
        self.id = id
        self.in_casino = False
        self.bankroll = None
        self.start_bankroll = self.bankroll
        self.gender = random.choice(['male', 'female'])
        self.name = names.get_full_name(gender=self.gender)
        self.age = random.randint(18,80)
        self.current_table = None
        self.customer_type = "normal"
        self.entry_atts_ = {"drunkness":random.randint(3,10),
                            "rage":random.randint(3,10),
                            "is_vip": random.choices([True,False], weights=(10,90), k=1)[0],
                            "has_weapon": random.choices([True,False], weights=(10,90), k=1)[0]} 
        self.min_bet_amount = 1
        self.casino: object = casino

    def enter_bouncer_queue(self):
        try:
            with self.casino.locks['bouncer']:
                self.casino.queues['bouncer']
                self.casino.LOG.info(f"{self.id} entered bouncer queue")
                return True
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)
            return False
        
    def check_status(self):
        if self in self.casino.customers:
            self.in_casino = True
            self.casino.LOG.info(f"{self.id} in casino")
            return True
        elif self in self.casino.customers_denied_entry:
            self.casino.LOG.info(f"{self.id} denied entry to casino")
            return False
        else:
            self.casino.LOG.info(f"{self.id} denied entryto casino")
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
        self.casino.LOG.info(f"{self.id} updating bankroll")
        self.bankroll += amount
        return self.bankroll
    
    def get_bankroll(self):
        return self.bankroll

    def bet(self, amount): 
        while amount < self.min_bet_amount:
            print(f"Bet placed: {amount}")
            if amount < self.min_bet_amount:
                print(f"Bet not enough for customer type , increasing bet by 300%...")
                amount *= 3
            print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
        self.bankroll -= amount

    def win(self, amount):
        self.bankroll += amount
    
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def goBathroom(self):
        if self.gender == "male":
            if len(self.casino.queues["bathrooms"]["male"]) < 5:
                with self.casino.locks['bathrooms']['male']:
                    self.casino.queues["bathrooms"]["male"].append(self)
                    print(f"{self.name} is using the bathroom...")
                    time.sleep(random.randrange(1, 20))
                    self.casino.queues["bathrooms"]["male"].remove(self)
                    print(f"{self.name} left the bathroom")
            else:
                print("Bathrooms are full, returning later.")
        if self.gender == "female":
            if len(self.casino.queues["bathrooms"]["female"]) < 10:
                with self.casino.locks['bathrooms']['female']:
                    self.casino.queues["bathrooms"]["female"].append(self)
                    print(f"{self.name} is using the bathroom...")
                    time.sleep(random.randrange(5, 20))
                    self.casino.queues["bathrooms"]["female"].remove(self)
                    print(f"{self.name} left the bathroom")
            else:
                print("Bathrooms are full, returning later.")

    def leave(self):
        if self in self.casino.customers:
            with self.casino.locks["customers"]:
                print(f"Customer {self.name} has left the casino.")
                self.casino.customers.remove(self)
                
    def update_customers(self, values:tuple, table='customers'):
        with self.casino.locks['db']:
            self.casino.database.insert_table(table, values)
<<<<<<< HEAD
    
    def enter_table_queue(self):
        with self.casino.locks['table']['customer']:
            self.casino.queues['table']['customer'].append(self)

    def leave_table(self):
        if self.current_table:
            self.current_table.current_customers.remove(self)
            
=======
>>>>>>> 20da578d6c13acbd6a68e33664ef35a8b614f958

    def run(self):
      # FIX 
        try:
            self.casino.LOG.info(f"Just created customer {self.id} thread")
            self.enter_bouncer_queue()
            if self.check_status() is True:
                self.update_customers(self, values=tuple(self.customer_id, name=self.name, age=self.age, gender=self.gender))
                while self.casino.is_open:
                    activity = random.choice(['play', 'drink', 'bathroom', 'observe'], weights=[0.6, 0.3, 0.05, 0.05], k=1)[0]

                    if activity.lower() == 'play':
                        self.enter_bouncer_queue()
                        time.sleep(30)
                        self.leave_table()

                    elif activity.lower() == 'drink':
                        self.casino.queues['bartender'].append(self)
                    elif activity.lower() == 'bathroom':
                        self.casino.bathrooms[self.gender].append(self)
                        self.goBathroom()
                    else:
                        time.sleep(random.randrange(5,10))
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)
           
        """
        at_the_door = True
        bouncer_found = False
        while at_the_door:
            self.casino.LOG.info(f"{self.id} is waiting in line to enter the Casino")
            self.casino.LOG.info(f"{self.id} is waiting for a bouncer")
            while not bouncer_found:
                for bouncer in self.casino.bouncers:
                    if bouncer.locks.locked():
                        time.sleep(2)
                        continue
                    bncr = bouncer
                    break
                bouncer_found = True
            entry = bncr.allow_entry(self)
            if not entry:
                return
            print(f"{self.name} has entered the casino.") 
            self.casino.customers.append(self) # Add self to casino list of customers
            at_the_door = False
        """


        while True:
            # EXIT CONDITIONS

            # Exit condition 1
            if self.isBankrupt():
                break
            # Exit condition 2
            if (self.bankroll > (self.start_bankroll*1.75)) or (self.bankroll < (self.start_bankroll*0.25)):
                break
            # Exit condition 3
            if self.games_played > 10:
                break

            # SELECT AN ACTIVITY 
            task_id = random.choices(["play", "bar", "bathroom"], weights=(60,20,10), k=1)[0]
            
            # SELECT A TABLE TO GO PLAY AT
            # if task_id == "play":
            #     table_chosen = random.choices(self.casino.tables, k=1)[0]
            #     append to table queue
                # CAREFUL, not all tables have play method, some have play()
                                    #   add table_type attribute to table classes to identify which method to use
                                    #   or create a consistent method for all
            
            # BAR
            if task_id == "bar":
                at_the_bar = True
                unattended = True
                while at_the_bar:
                    while unattended:
                        print(f"{self.name} is waiting at the bar")
                        for bartender in self.casino.bartenders:
                            if bartender.lock.locked():
                                continue
                            brt = bartender
                            unattended = False
                    print(f"{self.name} is being attended by bartender {brt.name}")
                    brt.take_order(self)
                    drink = brt.make_drink()
                    brt.serve_drink(self)
                    print(f"{self.name} enjoys the {drink}.")
                    time.sleep(5)
                    at_the_bar = False
                continue

            # BATHROOM
            if task_id == "bathroom":
                self.goBathroom()
                continue          


class HighRoller(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.bankroll = random.randint(5000000, 9999999)
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
        self.min_bet_amount = 10000
        self.customer_type = "medium_roller"


class LowRoller(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.bankroll = random.randint(10000,99999)
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

