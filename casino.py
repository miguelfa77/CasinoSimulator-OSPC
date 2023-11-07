import threading
import time
import random
import numpy as np

class Casino():
    # Attributes: coordinates
    def __init__(self, coordinates, tables=None, customers=None):
        for x in range(10):
            for y in range(10):
                self.coordinates[(x,y)] = ['queue b': '',y:]
        self.customer = 100
        self.tables = 10
        self.table_locks = {'table_queue':[], 'table_lock':threading.Lock()}

class Roulette(Casino):
    def __init__(self, casino : Casino):
        super().__init__()


