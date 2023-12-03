import random
import time
import names

class Dealer():
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
                with self.casino.locks['table']['dealer']:
                    self.current_table = table
                    return True
        else:
            return None
    
    def leave_table(self) -> None:
        for table in self.casino.tables:
            if self is table.current_dealer:
                with self.casino.locks['table']['dealer']:
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
            time.sleep(random.randrange(1,3))
        else:
            time.sleep(random.randrange(1,3))
   
    def run(self):
        self.casino.LOG.info(f"Running Dealer [{self.dealer_id}] thread")
        while self.casino.is_open:
            try:
                self.enter_table_queue()

                with self.casino.locks['table']['dealer']:
                    if self.check_table == True:
                        self.casino.LOG.info(f"Dealer [{self.dealer_id}]: Entered table [{self.current_table}]")
                        time.sleep(10)
                        random_choice = random.choice([self.take_break(), None])
                        if random_choice is not None and callable(random_choice):
                            random_choice()
                    else:
                        pass

            except Exception as e:
                self.casino.LOG.error(f"Error: {e}", exc_info=True)
            
        self.casino.LOG.info(f"Dealer [{self.dealer_id}]: Thread finished")





        


