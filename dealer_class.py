import threading
import random
import time
import names
from deck_class import NormalDeck, BlackJackDeck
from table_classes import Table

class Dealer(NormalDeck, BlackJackDeck):
    def __init__(self, id, tables : list[Table]) -> None:
        NormalDeck.__init__(self)
        BlackJackDeck.__init__(self)
        self.dealer_id = id   
        self.tables = tables    # table ID's list
        self.Name = names.get_first_name()
        self.Age = random.randint(18, 60)


    # Inherits functions:
    # - shuffle_deck()
    # - draw_card()
    
#    def take_bets(self, customer_id, quantity):
#        self.current_bets = 
#
#    def pay_winners(self, quantity, table : Table):
#        table.balance -= quantity
#        return table.balance
        

 #   def collect_losers(self, quantity, table : Table):
 #       table.balance += quantity
 #       return table.balance

    
    def take_break(self):
        time.sleep(random.randrange(5,10))
    
    def run(self):
    # Enter and leave queues
        while True:

            time.sleep(random.randrange(0,5))

            for table in self.tables:           # append if table queue is empty
                if not table['queue']:
                    with table.dealer['lock'].lock:
                        table.dealer['queue'].append(self.dealer_id)   
                    break
            else:                               # append to random table if not empty
                table = random.choice(self.tables)
                with table.dealer['lock'].lock:                        
                    table.dealer['queue'].append(self.dealer_id)

            time.sleep(20)

            self.take_break()



        


