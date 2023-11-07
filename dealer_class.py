import threading
import random
import time
import names
import random
from deck_class import Deck
from table_classes import Table

class Dealer(Deck):
    def __init__(self, id) -> None:
        self.dealer_id = id
        self.Name = names.get_first_name()
        self.Age = random.randint(18, 60)
        self.Lock = threading.Lock()

    # Inherits functions:
    # - shuffle_deck()
    # - draw_card()

    def take_bets(self, customer_id, quantity):
        current_bets[customer_id] =  quantity

    def pay_winners(self, quantity, table : Table) -> int:
        table.balance -= quantity
        return table.balance
        

    def collect_losers(self, quantity, table : Table) -> int:
        table.balance += quantity
        return table.balance

