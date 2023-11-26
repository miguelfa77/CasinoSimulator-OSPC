import threading
import concurrent.futures
import random
from classes_file import Roulette, Blackjack, Poker, Dealer, Bartender, Bouncer, customer_type

class Casino:

    _instance = None

    def __init__(self,STARTING_BALANCE,NUM_OF_TABLES,NUM_OF_CUSTOMERS,NUM_OF_DEALERS,NUM_OF_BARTENDERS,NUM_OF_BOUNCERS) -> None:
        """
        :Params: starting balance, number of tables, customers, dealers, bartenders, bouncers
        Note: Numbers can be made so the user inputs them more alike an actual simulation. 
        """
        self._balance = STARTING_BALANCE
        self._NUM_OF_TABLES = NUM_OF_TABLES
        self._NUM_OF_CUSTOMERS = NUM_OF_CUSTOMERS     # accessed by bouncer class
        self._NUM_OF_DEALERS = NUM_OF_DEALERS
        self._NUM_OF_BARTENDERS = NUM_OF_BARTENDERS
        self._NUM_OF_BOUNCERS = NUM_OF_BOUNCERS

        self.customers = []
        self.tables = []
        self.dealers = []
        self.bartenders = []
        self.bouncers = []
        self.bathrooms = {"male": [],
                          "female": []}
        
        #self.log_file = 'casino_log.txt'
        self.opening_time = 0
        self.closing_time = 1000
        self.lock = {'customer': threading.Lock(),
                      'balance': threading.Lock()}
        self.is_open = True
        self.initialize_internal()   

    def __new__(cls):
        """
        :returns: the same intance if already instantiated.
        :extra: initialize_internal() -> instantiates all internal and appends to class attribute lists.
        """
        if not cls._instance:
            cls._instance = super(Casino, cls).__new__(cls)
        return cls._instance

    
    def initialize_internal(self):
        """
        Initialize and append to shared class variables: tables, dealer, bartenders, bounces
        """
        tables = [(Roulette(table_id, self), Blackjack(table_id+1, self), Poker(table_id+2, self)) for table_id in range(self._NUM_OF_TABLES)]
        self.tables.extend(tables)

        dealers = [Dealer(dealer_id, self) for dealer_id in range(self._NUM_OF_DEALERS)]
        self.dealers.extend(dealers)

        bartenders = [Bartender(bartender_id, self) for bartender_id in range(self._NUM_OF_BARTENDERS)]
        self.bartenders.extend(bartenders)
        
        bouncers = [Bouncer(bouncer_id, self) for bouncer_id in range(self._NUM_OF_BOUNCERS)]
        self.bouncers.extend(bouncers)

    def initialize_external(self):
        """
        Initialize but not append to global/shared variables of the casino.
        """
        customer_choices = random.choices(['high','medium','low'], weights=[0.2, 0.5, 0.3], k=self._NUM_OF_CUSTOMERS)

        customers = [customer_type(index, choice) for index, choice in enumerate(customer_choices)]
        return customers
    
    
    @staticmethod
    def casino_info(func):
        def print_balance(self, amount, executor:object):
            if executor:
                print(f'[{executor.__class__.__name__}] updated casino balance by: [{amount}]')
                return func(self, amount)
            else:
                print(f'[Unknown] updated casino balance by: [{amount}]')
        return print_balance

 
    @casino_info
    def update_balance(self, amount, executor:object=None):
        """
        :params: amount: int (positive or negative)
        Performs the balance update.
        Note: Other classes (e.g. table) can update balance without directly accessing the 'private' _balance var.
        """
        with self.lock['balance']:
            self._balance += amount

    def get_balance(self):
        """
        :returns: casino balance in case it wants to be printed or smth
        """
        return self._balance


    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=(self._NUM_OF_BARTENDERS+self._NUM_OF_BOUNCERS+self._NUM_OF_DEALERS+self._NUM_OF_TABLES)) as exe:
            table_threads = [exe.submit(table.run) for table in self.tables]
            dealer_threads = [exe.submit(dealer.run) for dealer in self.dealers]
            bartender_threads = [exe.submit(bartender.run) for bartender in self.bartenders]
            bouncer_theads = [exe.submit(bouncer.run) for bouncer in self.bouncers]

        print(f"The Casino is now open.")
        customers = self.initialize_external()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._NUM_OF_CUSTOMERS) as exe2:
            customer_threads = [exe2.submit(customer.run) for customer in customers]


        while self.is_open:
            pass
        
        self.is_open = False
        # CHECK ALL THREADS ARE DEAD WITH is_alive()
        print(f"casino is now closed.")


    