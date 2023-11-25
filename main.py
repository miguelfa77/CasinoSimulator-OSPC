import threading
import time
import random
import numpy as np
import concurrent.futures
from casino_class import Casino
from dealer_class import Dealer
from table_classes import Blackjack, Roulette, Poker
from customer_classes import Customer
from bartender_class import Bartender
from bouncer_class import Bouncer
from deck_class import NormalDeck, BlackJackDeck

if __name__ == "__main__":
    starting_balance = 10000000
    NUM_OF_TABLES = 10
    NUM_OF_CUSTOMERS = 100
    NUM_OF_DEALERS = 10
    NUM_OF_BARTENDERS = 5
    NUM_OF_BOUNCERS = 2

    casino = Casino(starting_balance)

    with concurrent.futures.ThreadPoolExecutor(num_workers=1) as exe:
        exe.submit(casino.run)
        with concurrent.futures.ThreadPoolExecutor(num_workers=range(num_of_tables)) as exe:
            for table in tables:
                exe.submit(table.run)
            with concurrent.futures.ThreadPoolExecutor(num_workers=range(num_of_customers)) as exe1:
                for customer in customers:
                    exe.submit(customer.run)
        







