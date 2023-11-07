import threading
import random
import time
import names
import random

class Dealer(Deck):
    def __init__(self) -> None:
        self.Name = names.get_first_name()
        self.Age = random.randrange(18, 60)






        
