from classes.customer_classes import Customer
import random
import names
import time

"""
- Bouncers share the same queue
- Add customer attr. to the customer class
- Possibility: Initilize only the Bouncer instances with customers as constructors and append to 
"""

class Bouncer:

    def __init__(self, id, casino: object):
        self.bouncer_id = id
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
        self.current_customer = None
        self.vip_list = set()
        self.casino: object = casino
    
    def check_id(self, customer:Customer):
        if customer.age < 18:
            return False
        return True

    def check_drunkenness(self, customer:Customer):
        if customer.entry_atts_['drunkness'] > 5:
            return False
        return True

    def check_rage(self, customer:Customer):
        if customer.entry_atts_['rage'] > 5:
            return False
        return True

    def check_weapons(self, customer:Customer):
        if customer.entry_atts_['has_weapon']:
            return False
        return True

    def check_vip(self, customer:Customer):
        need_to_check = random.choices([True, False], weights=(10,90), k=1)[0]
        if not need_to_check:
            return True
        if customer.entry_atts_['is_vip']:
            print(f"Welcome back, VIP {customer.name}! Please enjoy your stay.")
            return True
        return False

    def kick_out(self, customer:Customer, reason=None):
        self.casino.LOG.info(f'Customer [{customer.id}] kicked out')
        self.casino.customers_denied_entry.append(customer)

    def allow_entry(self, customer:Customer):
        if self.check_id(customer) and self.check_drunkenness(customer) and self.check_rage(customer) and self.check_weapons(customer):
            return True
        else:
            return False
            
    def run(self):
        self.casino.LOG.info(f"Running bouncer [{self.bouncer_id}] thread")
        while self.casino.is_open:
            time.sleep(2)
            try:
                if self.casino.queues['bouncer']:
                    with self.casino.locks['bouncer']:
                        self.current_customer = self.casino.queues['bouncer'].pop()
                        if self.allow_entry(self.current_customer):
                            self.casino.LOG.debug(f"Bouncer [{self.bouncer_id}] allowed customer [{self.current_customer.id}] to enter")
                            with self.casino.locks['customer']:
                                self.casino.customers.append(self.current_customer)
                        else:
                            self.kick_out(self.current_customer) 
            except Exception as e:
                self.casino.LOG.error(f"Error: {e}", exc_info=True)

                


            
