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
    """
    Subject to change if we want to use inputs instead of predefined constants. 
    Keep like this for now.
    """

    starting_balance = 100000000
    NUM_OF_TABLES = 10
    NUM_OF_CUSTOMERS = 100
    NUM_OF_DEALERS = 10
    NUM_OF_BARTENDERS = 5
    NUM_OF_BOUNCERS = 2

    casino = Casino(STARTING_BALANCE=starting_balance,
                    NUM_OF_TABLES=NUM_OF_TABLES,
                    NUM_OF_CUSTOMERS=NUM_OF_CUSTOMERS,
                    NUM_OF_DEALERS=NUM_OF_DEALERS,
                    NUM_OF_BARTENDERS=NUM_OF_BARTENDERS,
                    NUM_OF_BOUNCERS=NUM_OF_BOUNCERS)

    casino.run()







