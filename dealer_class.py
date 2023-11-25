import threading
import random
import time
import names
from deck_class import *
from casino_class import Casino
from typing import Optional

class Dealer(Deck):
    """
    :methods: shuffle_deck, draw_card, take_break, run
    :params: id, tables : list of Table instances
    """
    def __init__(self, id) -> None:
        self.dealer_id = id 
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)  
        self.current_table = None
        self.casino = Casino()
    
    def leave_table(self):
        try:
            if self.dealer_id in self.current_table.dealer['queue']:
                with self.current_table.dealer['lock']:
                    self.current_table['queue'].remove(self)
            elif self.dealer_id == self.current_table.current_dealer:
                with self.current_table.dealer['lock']:
                    self.current_table.current_dealer = None
        except:
            print('Cant find dealer at current table')
         
    def take_break(self):
        if self.current_table:
            self.leave_table()
            time.sleep(random.randrange(2,5))
        else:
            time.sleep(random.randrange(2,5))

    def enter_table_queue(self):
        """
        Accesses via casino instance
        :returns: table_id (where dealer is) or None
        """
        try:
            for table in self.casino.tables:           # append if table queue is empty
                if not table['queue']:
                    with table.dealer['lock']:
                        table.dealer['queue'].append(self)
                        return table  
            else:                               # append to random table if not empty
                table = random.choice(self.casino.tables)
                with table.dealer['lock']:                        
                    table.dealer['queue'].append(self)
                    return table
        except:
            return None
   
    def run(self):
        while self.casino.is_open:
            try:
                time.sleep(random.randrange(0,5))

                self.current_table = self.enter_table_queue()

                if self.current_table:
                    time.sleep(20)
                    random_choice = random.choice(self.take_break(), None)
                    if random_choice is not None and callable(random_choice):
                        random_choice()
                else:
                    continue
                     
            except Exception as e:
                print(e)





        


