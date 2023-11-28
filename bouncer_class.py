from customer_classes import Customer
import random
import names

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
        need_to_check = random.choices([True, False], weights=(10,90), k=1)[0]
        if not need_to_check:
            return True
        if customer.entry_atts_['is_vip']:
            print(f"Welcome back, VIP {customer.name}! Please enjoy your stay.")
            return True
        return False

    def kick_out(self, customer:Customer, reason):
        print(f"Customer {customer.name} has been kicked out for {reason}.")
        self.kicked_out_customers.append(customer)

    def allow_entry(self, customer:Customer):
        if self.check_vip(customer) and self.check_id(customer) and self.check_drunkenness(customer) and self.check_rage(customer) and self.check_weapons(customer):
            print(f"Customer {customer.name} is allowed to enter.")
            return True
        else:
            return False
            
    def run(self):
        try:
            while self.casino.is_open:
                if self.casino.queues['bouncer']:
                    with self.locks['bouncer']:
                        self.current_customer = self.casino.queues['bouncer'].pop()
                        if self.allow_entry(self.current_customer):
                            with self.casino.locks['customer']:
                                self.casino.customers.append(self.current_customer)
                        else:
                            self.kicked_out_customers.append(self.current_customer)
                
                else:
                    pass
        except:
            print("Error in Bouncer")

                


            
