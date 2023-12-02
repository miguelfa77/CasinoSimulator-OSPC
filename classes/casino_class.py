import threading
import concurrent.futures
import random
import time
from classes.classes_file import (
    Roulette,
    BlackJack,
    Poker,
    Dealer,
    Bartender,
    Bouncer,
    customer_type,
    casinoDB,
    myLogger,
)


class Casino:
    _instance = None

    def __new__(cls):
        """
        :returns: the same intance if already instantiated.
        """
        if not cls._instance:
            cls._instance = super(Casino, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        STARTING_BALANCE,
        NUM_OF_TABLES,
        NUM_OF_CUSTOMERS,
        NUM_OF_DEALERS,
        NUM_OF_BARTENDERS,
        NUM_OF_BOUNCERS,
    ) -> None:
        """
        :params: starting balance, number of: tables, customers, dealers, bartenders, bouncers.
        Note: Numbers can be made so the user inputs them more alike an actual simulation.
        :extra: initialize_internal() -> instantiates all internal and appends to instance attribute lists.
        """
        self._SIM_DURATION = 1000
        self._balance = STARTING_BALANCE
        self._NUM_OF_TABLES = NUM_OF_TABLES
        self._NUM_OF_CUSTOMERS = NUM_OF_CUSTOMERS  # accessed by bouncer class
        self._NUM_OF_DEALERS = NUM_OF_DEALERS
        self._NUM_OF_BARTENDERS = NUM_OF_BARTENDERS
        self._NUM_OF_BOUNCERS = NUM_OF_BOUNCERS

        self.LOG = myLogger()
        self.database = casinoDB()
        self.customers = []
        self.customers_denied_entry = []
        self.tables = []
        self.dealers = []
        self.bartenders = []
        self.bouncers = []
        self.vip = {"queue": [], "lock": threading.Lock()}
        self.queues = {
            "table": {"dealer": [], "customer": []},
            "bartender": [],
            "bouncer": [],
            "bathroom": {"male": [], "female": []},
        }
        self.locks = {
            "balance": threading.Lock(),
            "db": threading.Lock(),
            "table": {"dealer": threading.Lock(), "customer": threading.Lock()},
            "bartender": threading.Lock(),
            "bouncer": threading.Lock(),
            "customer": threading.Lock(),
            "bathroom": {"male": threading.Lock(), "female": threading.Lock()},
        }
        self.opening_time = 0
        self.closing_time = 1000
        self.is_open = True
        self.initialize_internal()

    def initialize_internal(self):
        """
        Initialize and append to shared class variables: tables, dealer, bartenders, bounces
        """
        """
        tables = [Roulette(table_id, self) for table_id in range(0, self._NUM_OF_TABLES, 3)] + \
                [BlackJack(table_id+1, self) for table_id in range(0, self._NUM_OF_TABLES, 3)] + \
                [Poker(table_id+2, self) for table_id in range(0, self._NUM_OF_TABLES, 3)]
        """
        poker = [Poker(table_id, self) for table_id in range(0, self._NUM_OF_TABLES)]
        roulette = [Roulette(table_id + 1, self) for table_id in range(0, self._NUM_OF_TABLES)]
        bj = [BlackJack(table_id + 2, self) for table_id in range(0, self._NUM_OF_TABLES)]
        tables = poker + roulette + bj
        self.tables.extend(tables)
        self.LOG.info(f"Tables List: {tables}")

        dealers = [Dealer(dealer_id, self) for dealer_id in range(self._NUM_OF_DEALERS)]
        self.dealers.extend(dealers)
        self.LOG.info(f"Dealers List: {dealers}")

        bartenders = [
            Bartender(bartender_id, self) for bartender_id in range(self._NUM_OF_BARTENDERS)
        ]
        self.bartenders.extend(bartenders)
        self.LOG.info(f"Bartenders List: {bartenders}")

        bouncers = [Bouncer(bouncer_id, self) for bouncer_id in range(self._NUM_OF_BOUNCERS)]
        self.bouncers.extend(bouncers)
        self.LOG.info(f"Bouncers List: {bouncers}")

    def initialize_external(self):
        """
        Initialize but not append to global/shared variables of the casino.
        """
        customer_choices = random.choices(
            ["high", "medium", "low"], weights=[0.2, 0.5, 0.3], k=self._NUM_OF_CUSTOMERS
        )

        customers = [
            customer_type(id=index, type=choice, casino=self)
            for index, choice in enumerate(customer_choices)
        ]
        return customers

    @staticmethod
    def update_transactions(func):
        def transactions_append(self, amount, executor: object, table="transactions"):
            with self.locks["db"]:
                self.database.insert_table(table=table, values=tuple([executor, amount]))
            return func(self, amount, executor, table)

        return transactions_append

    @update_transactions
    def update_balance(self, amount, executor: object, table="transactions"):
        """
        :params: amount: int (positive or negative)
        Performs the balance update.
        Note: Other classes (e.g. table) can update balance without directly accessing the 'private' _balance var.
        """
        with self.locks["balance"]:
            self._balance += amount

    def get_balance(self):
        """
        :returns: casino balance in case it wants to be printed or smth
        """
        return self._balance

    def run(self):
        print("Starting thread")
        self.LOG.info("Starting Thread")

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=(
                self._NUM_OF_BARTENDERS
                + self._NUM_OF_BOUNCERS
                + self._NUM_OF_DEALERS
                + self._NUM_OF_TABLES
                + self._NUM_OF_CUSTOMERS
            )
        ) as exe:
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
            self.LOG.info(f"Initialized customers: {customers}")
            customer_threads = [exe.submit(customer.run) for customer in customers]
            self.LOG.info(f"Initialized customer threads: {customer_threads}")

            while elapsed_time <= self._SIM_DURATION:
                elapsed_time = time.time() - start_time

            self.is_open = False
            self.LOG.info("The Casino is now closed.")
