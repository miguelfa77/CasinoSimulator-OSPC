import threading
import time
import random
import numpy as np
import concurrent.futures
from casino_class import Casino
from dealer_class import Dealer
from table_classes import Blackjack, Roulette, Poker
from customer_classes import Customer, HighSpender, MediumSpender, LowSpender
from bartender_class import Bartender
from bouncer_class import Bouncer
from deck_class import NormalDeck, BlackJackDeck

if __name__ == "__main__":
    starting_balance = 1000000
    num_of_tables = 10
    num_of_customers = 100
    num_of_dealers = 10
    num_of_bartenders = 5
    num_of_bouncers = 2

    customers = [Customer(id) for id in range(num_of_customers)]
    tables = [(Blackjack(id, BlackJackDeck), Roulette(id+1), Poker(id+2, NormalDeck)) for id in range(0, num_of_tables, 2)]
    dealers = [Dealer(id, tables) for id in range(num_of_dealers)]
    bartenders = [Bartender(id) for id in range(num_of_bartenders)]
    bouncers = [Bouncer(id) for id in range(num_of_bouncers)]
    casino = Casino(starting_balance, customers, tables, bartenders, bouncers)

    with concurrent.futures.ThreadPoolExecutor(num_workers=len(range(num_of_tables))) as exe:
        for table in tables:
            exe.submit(table.run)
        with concurrent.futures.ThreadPoolExecutor(num_workers=len(range(num_of_customers))) as exe1:
            for customer in customers:
                exe.submit(customer.run, casino)
        







