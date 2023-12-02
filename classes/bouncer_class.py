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
        self.vip_list = set()  # List of VIP customer names
        self.casino: object = casino
    
    def check_id(self, customer:Customer):
        if customer.age < 18:
            self.kick_out(customer, reason='underage')
            return False
        return True

    def check_drunkenness(self, customer:Customer):
        if customer.entry_atts_['drunkness'] > 5:
            self.kick_out(customer, reason='too drunk')
            return False
        return True

    def check_rage(self, customer:Customer):
        if customer.entry_atts_['rage'] > 5:
            self.kick_out(customer, reason='raging')
            return False
        return True

    def check_weapons(self, customer:Customer):
        if customer.entry_atts_['has_weapon']:
            self.kick_out(customer, reason='carrying a weapon')
            return False
        return True

    def check_vip(self, customer:Customer):
        if customer.entry_atts_['is_vip']:
            print(f"Welcome back, VIP {customer.name}! Please enjoy your stay.")
            return True
        return False

    def kick_out(self, customer:Customer, reason):
        self.casino.LOG.info(f'Customer [{customer}] kicked out')
        self.kicked_out_customers.append(customer)

    def allow_entry(self, customer:Customer):
        if self.check_vip(customer):
            return True
        if self.check_id(customer) and self.check_drunkenness(customer) and self.check_rage(customer) and self.check_weapons(customer):
            return True
        else:
            return False
            
    def run(self):
        try:
            while self.casino.is_open:
                if self.casino.queues['bouncer']:
                    with self.casino.locks['bouncer']:
                        self.current_customer = self.casino.queues['bouncer'].pop()
                        if self.allow_entry(self.current_customer):
                            with self.casino.locks['customer']:
                                self.casino.customers.append(self.current_customer)
                        else:
                            with self.casino.locks['customer']:
                                self.kicked_out_customers.append(self.current_customer)
                
                else:
                    time.sleep(.5)
                    continue
        except Exception as e:
            self.casino.LOG.error(f"Error: {e}", exc_info=True)

                


            
