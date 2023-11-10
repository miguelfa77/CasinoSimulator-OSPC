import random
import threading 

Class Tables(threading.Thread):

        def __init__(self,balance):
                super().__init__()
                self.balance = balance 
                print(f"The balance of the Casino is", balance)
                self.lock = threading.Lock()
        def run(self):
                self.lock.acquire()
                time.sleep(3)
                self.lock.release()







        
