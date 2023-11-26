# Bouncer class

import time
import threading
import random

class Bouncer:
    def __init__(self, id):
        self.bouncer_id = id
        self.kicked_out_customers = []
        self.vip_list = set()  # List of VIP customer names
        self.lock = threading.Lock()

    def check_id(self, customer):
        if customer.age < 18:
            print(f"Customer {customer.name} has been kicked out for being underage.")
            return False
        return True

    def check_drunkenness(self, customer):
        if customer.entry_atts_["drunkness"] > 5:
            print(f"Customer {customer.name} has been kicked out for too drunk.")
            return False
        return True

    def check_rage(self, customer):
        if customer.entry_atts_['rage'] > 5:
            print(f"Customer {customer.name} has been kicked out for raging.")
            return False
        return True

    def check_weapons(self, customer):
        if customer.entry_atts_['has_weapon']:
            print(f"Customer {customer.name} has been kicked out for carrying a weapon.")
            return False
        return True

    def check_vip(self, customer):
        need_to_check = random.choices([True, False], weights=(10,90), k=1)[0]
        if not need_to_check:
            return True
        if customer.entry_atts_["is_vip"]:
            print(f"Welcome back, VIP {customer.name}! Please enjoy your stay.")
            return True
        return False

    def allow_entry(self, customer):
        with self.lock:
            if self.check_vip(customer) and self.check_id(customer) and self.check_drunkenness(customer) and self.check_rage(customer) and self.check_weapons(customer):
                print(f"Customer {customer.name} is allowed to enter.")
                return True
            else:
                return False
        
