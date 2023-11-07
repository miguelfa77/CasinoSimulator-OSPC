import threading
import random
import time
import names
import random

class Table:
    def __init__(self):
        self.Name = names.get_first_name()
        self.Age = random.randrange(18, 60)

    def deal_cards():
