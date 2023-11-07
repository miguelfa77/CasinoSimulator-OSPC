import threading
import random
import time
import names
import random
from deck_class import Deck

class Dealer(Deck):
    def __init__(self, id) -> None:
        self.dealer_id = id
        self.Name = names.get_first_name()
        self.Age = random.randint(18, 60)
        self.Lock = threading.Lock()

    # Inherits functions:
    # - shuffle_deck()
    # - draw_card()
