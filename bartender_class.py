import random
import names

class Bartender:
    def __init__(self):
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)
