import threading
import time
import random
import numpy as np
import concurrent.futures
from casino_class import Casino
from dealer_class import Dealer
from table_classes import Table
from customer_classes import Customer

if __name__ == "__main__":
    casino = Casino(starting_balance=1000000)
    customers = [Customer(id) for id in range(random.randrange(50,100))]
    with concurrent.futures.ThreadPoolExecutor(num_workers=range(customers)) as exe:
        for customer in customers:
            exe.submit(customer.run)
            






