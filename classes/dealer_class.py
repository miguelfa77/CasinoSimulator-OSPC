import random
import time
import names
from classes.deck_class import Deck

class Dealer(Deck):
    """
    :methods: shuffle_deck, draw_card, take_break, run
    :params: id, tables : list of Table instances
    """
    def __init__(self, id, casino: object) -> None:
        self.dealer_id = id 
        self.name = names.get_first_name()
        self.age = random.randint(18, 60)  
        self.current_table = None
        self.casino: object = casino


    def enter_table_queue(self):
        """
        Accesses via casino instance
        :returns: table_id (where dealer is) or None
        """
        with self.casino.locks['table']['dealer']:
            self.casino.queues['table']['dealer'].append(self)

    def check_table(self):
        for table in self.casino.tables:
            if self is table.current_dealer:
                self.current_table = table
                return True
        else:
            return None
    
    def leave_table(self) -> None:
        for table in self.casino.tables:
            if self is table.current_dealer:
                table.current_dealer = None
                return True
        if self in self.casino.queues['table']['dealer']:
            with self.casino.locks['table']['dealer']:
                self.casino.queues['table']['dealer'].remove(self)
                return True
        else:
            return False
         
    def take_break(self) -> None:
        if self.current_table:
            self.leave_table()
            time.sleep(random.randrange(2,5))
        else:
            time.sleep(random.randrange(2,5))
   
    def run(self):
        while self.casino.is_open:
            try:
                time.sleep(random.randrange(0,5))

                self.enter_table_queue()

                if self.check_table:
                    time.sleep(20)
                    random_choice = random.choice([self.take_break(), None])
                    if random_choice is not None and callable(random_choice):
                        random_choice()
                else:
                    continue
                     
            except Exception as e:
                print(e)





        


