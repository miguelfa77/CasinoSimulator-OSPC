import threading
import concurrent.futures
import random
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import sys
from classes.classes_file import Roulette, BlackJack, Poker, Dealer, Bartender, Bouncer, customer_type, casinoDB, myLogger

class Casino:

    _instance = None

    def __new__(cls):
        """
        :returns: the same intance if already instantiated.
        """
        if not cls._instance:
            cls._instance = super(Casino, cls).__new__(cls)
        return cls._instance

    def __init__(self,STARTING_BALANCE,SIM_DURATION, NUM_OF_TABLES,NUM_OF_CUSTOMERS,NUM_OF_DEALERS,NUM_OF_BARTENDERS,NUM_OF_BOUNCERS) -> None:
        """
        :params: starting balance, number of: tables, customers, dealers, bartenders, bouncers.
        Note: Numbers can be made so the user inputs them more alike an actual simulation.
        :extra: initialize_internal() -> instantiates all internal and appends to instance attribute lists. 
        """
        self._SIM_DURATION = SIM_DURATION
        self.starting_balance = STARTING_BALANCE
        self._balance = STARTING_BALANCE
        self._NUM_OF_TABLES = NUM_OF_TABLES
        self._NUM_OF_CUSTOMERS = NUM_OF_CUSTOMERS  
        self._NUM_OF_DEALERS = NUM_OF_DEALERS
        self._NUM_OF_BARTENDERS = NUM_OF_BARTENDERS
        self._NUM_OF_BOUNCERS = NUM_OF_BOUNCERS
        self.sim_params = f'\n\n{"*" * 10} Duration: {self._SIM_DURATION} | Starting Balance: {self.starting_balance} {"*" * 10}\n ' + \
        f'Tables: {self._NUM_OF_TABLES} | Dealers: {self._NUM_OF_DEALERS} | Bouncers: {self._NUM_OF_BOUNCERS} | Bartenders: {self._NUM_OF_BARTENDERS} | Customers: {self._NUM_OF_CUSTOMERS}\n\n'

        self.LOG = myLogger()
        self.database = casinoDB(self)
        self.customers = []
        self.customers_denied_entry = []
        self.tables = []
        self.dealers = []
        self.bartenders = []
        self.bouncers = []
        self.queues = {'table':{'dealer':[], 'customer': []}, 
                       'bartender': [],
                       'bouncer': [],
                       'bathroom':{'male': [],
                                    'female': []}
                       }
        self.locks = {'balance': threading.Lock(),
                      'db': threading.Lock(),
                      'table':{'dealer': threading.Lock(), 'customer': threading.Lock()}, 
                       'bartender': threading.Lock(),
                       'bouncer': threading.Lock(),
                       'customer': threading.Lock(),
                       'bathroom':{'male': threading.Lock(),
                                    'female': threading.Lock()}

                       }
        self.opening_time = 0
        self.closing_time = 1000
        self.is_open = True
        self.initialize_internal()   

    
    def initialize_internal(self):
        """
        Initialize and append to shared class variables: tables, dealers, bartenders, bouncers
        """
    
        tables = [Roulette(table_id, self) for table_id in range(0, self._NUM_OF_TABLES, 3)] + \
                [BlackJack(table_id+1, self) for table_id in range(0, self._NUM_OF_TABLES, 3)] + \
                [Poker(table_id+2, self) for table_id in range(0, self._NUM_OF_TABLES, 3)]
        
        self.tables.extend(tables)
        self.LOG.info(f"Tables List: {tables}")

        dealers = [Dealer(dealer_id, self) for dealer_id in range(self._NUM_OF_DEALERS)]
        self.dealers.extend(dealers)
        self.LOG.info(f"Dealers List: {dealers}")

        bartenders = [Bartender(bartender_id, self) for bartender_id in range(self._NUM_OF_BARTENDERS)]
        self.bartenders.extend(bartenders)
        self.LOG.info(f"Bartenders List: {bartenders}")
        
        bouncers = [Bouncer(bouncer_id, self) for bouncer_id in range(self._NUM_OF_BOUNCERS)]
        self.bouncers.extend(bouncers)
        self.LOG.info(f"Bouncers List: {bouncers}")

    def initialize_external(self):
        """
        Initialize but not append to global/shared variables of the casino.
        """
        customer_choices = random.choices(['high','medium','low'], weights=[0.2, 0.5, 0.3], k=self._NUM_OF_CUSTOMERS)

        customers = [customer_type(id=index, type=choice, casino=self) for index, choice in enumerate(customer_choices)]
        return customers
    
    
    @staticmethod
    def update_transactions(func):
        def transactions_append(self, amount, executor:object, table='transactions'):
            self.database.insert_table(table=table, values=tuple([executor, amount]))
            return func(self, amount, executor, table)
        return transactions_append

 
    @update_transactions
    def update_balance(self, amount, executor:object, table='transactions'):
        """
        :params: amount: int (positive or negative)
        Performs the balance update.
        Note: Other classes (e.g. table) can update balance without directly accessing the 'private' _balance var.
        """
        with self.locks['balance']:
            self._balance += amount

    def get_balance(self):
        """
        :returns: casino balance in case it wants to be printed or displayed
        """
        return self._balance
    
    def plot_balance(self):
        data = self.database.fetch_table('transactions')
        for entry in data:
            amount = entry[0]
            timestamp = entry[1]
        

        amount = []
        timestamp = []
        for entry in data:
            amount.append(entry[0] )
            timestamp.append(entry[1])
        amount = np.cumsum(amount)

        plt.plot(timestamp, amount)
        plt.xlabel('timestamp')
        plt.ylabel('cumulative amount ($)')
        plt.suptitle('Casino Profit and Loss (PnL)', fontsize=15, fontweight='bold', color='black',horizontalalignment='center')
        plt.title(f'Sim Params - [Duration: {self._SIM_DURATION}, Starting Balance: {self.starting_balance}]', fontsize=10, fontweight='demibold')
        plt.xticks(rotation=300)
        plt.axhline(y=0, color='red', linestyle='--')
        plt.tight_layout()
        plt.savefig('CasinoPerformance.png')
        plt.show()
        
    
    def run(self):
        self.LOG.info(self.sim_params)
        self.LOG.info('Starting Main Thread')
        self.update_balance(amount=0, executor=Casino)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=(self._NUM_OF_BARTENDERS+self._NUM_OF_BOUNCERS+self._NUM_OF_DEALERS+self._NUM_OF_TABLES+self._NUM_OF_CUSTOMERS)) as exe:
            table_threads = [exe.submit(table.run) for table in self.tables]
            dealer_threads = [exe.submit(dealer.run) for dealer in self.dealers]
            bartender_threads = [exe.submit(bartender.run) for bartender in self.bartenders]
            bouncer_threads = [exe.submit(bouncer.run) for bouncer in self.bouncers]
            self.LOG.info(f"Table threads: {table_threads}")
            self.LOG.info(f"Dealer threads: {dealer_threads}")
            self.LOG.info(f"Bartender threads: {bartender_threads}")
            self.LOG.info(f"Bouncer threads: {bouncer_threads}")

            start_time = time.time()
            elapsed_time = 0
            self.LOG.info("The Casino is now open.")

            customers = self.initialize_external()
            customer_threads = [exe.submit(customer.run) for customer in customers]
            self.LOG.info(f"Initialized customer threads: {customer_threads}")

            while elapsed_time <= self._SIM_DURATION:
                elapsed_time = time.time() - start_time
    
            self.is_open = False

        exe.shutdown()

        self.LOG.info(f"The Casino is now closed.")

        self.plot_balance()

        sys.exit()


    