import random
import threading 

num_players = random.randrange(1, 5)
casino_balance = 100000

class Tables(threading.Thread):

        def __init__(self,balance):
                super().__init__()
                self.balance = balance 
                print(f"The balance of the Casino is", balance)
                tables_lock = threading.Lock()
        def run(self):
                self.lock.acquire()
                time.sleep(3)
                self.lock.release()
        
        def roulette(player_id):
            global casino_balance
        
            with casino_lock:
                if casino_balance <= 0:
                    print(f"Player {player_id} can't bet. Insufficient balance. Balance of the casino: ${casino_balance}")
                    return
        
                num_bets = random.randint(1, 12)  # Let's allow the player to place 1 to 5 bets.
                total_winnings = 0
        
                for _ in range(num_bets):
                    bet_amount = random.randrange(10, 1000)  # Bet a random amount within the available balance.
                    number_bet = random.randrange(0, 36)
                    outcome = random.randrange(0, 36)
        
                    if outcome == number_bet:
                        winnings = bet_amount * 36
                        casino_balance -= winnings
                        total_winnings += winnings
                        print(f"Player {player_id} wins ${winnings} on number {number_bet}!")
                    else:
                        casino_balance += bet_amount
                        total_winnings -= bet_amount
                        print(f"Player {player_id} loses ${bet_amount} on number {number_bet}!")
        
                print(f"Player {player_id} results: Net worth: ${total_winnings}, Balance of the casino: ${casino_balance}")

player_threads = []
for i in range(num_players):
    player_thread = threading.Thread(target=roulette, args=(i,))
    player_threads.append(player_thread)

for thread in player_threads:
    thread.start()

for thread in player_threads:
    thread.join()

print(f"Final Casino Balance: ${casino_balance}")






        
