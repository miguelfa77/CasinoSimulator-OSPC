class Customer:
    def __init__(self, name, age, drunkenness, rage, is_vip=False, has_weapon=False):
        self.name = name
        self.age = age
        self.drunkenness = drunkenness
        self.rage = rage
        self.is_vip = is_vip
        self.has_weapon = has_weapon
class Bouncer:
    def __init__(self, id):
        self.bouncer_id = id
        self.kicked_out_customers = []
        self.vip_list = set()  # A set of VIP customer names

    def check_id(self, customer):
        if customer.age < 18:
            self.kick_out(customer, reason="underage")
            return False
        return True

    def check_drunkenness(self, customer):
        if customer.drunkenness > 5:
            self.kick_out(customer, reason="too drunk")
            return False
        return True

    def check_rage(self, customer):
        if customer.rage > 5:
            self.kick_out(customer, reason="raging")
            return False
        return True

    def check_weapons(self, customer):
        if customer.has_weapon:
            self.kick_out(customer, reason="carrying a weapon")
            return False
        return True

    def check_vip(self, customer):
        if customer.is_vip:
            print(f"Welcome back, VIP {customer.name}! Please enjoy your stay.")
            return True
        return False

    def kick_out(self, customer, reason):
        print(f"Customer {customer.name} has been kicked out for {reason}.")
        self.kicked_out_customers.append(self.customer)

    def allow_entry(self, customer):
        if self.check_vip(customer):
            return True
        if not self.check_id(customer):
            return False
        if not self.check_drunkenness(customer):
            return False
        if not self.check_rage(customer):
            return False
        if not self.check_weapons(customer):
            return False
        print(f"Customer {customer.name} is allowed to enter. Enjoy your visit!")
        return True

