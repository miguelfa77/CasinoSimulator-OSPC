import threading
import random
import time

# Casino lock
casino_lock = threading.Lock()

# Casino balance
casino_balance = 100000

# Number of players
num_players = random.randrange(1, 5)

# Roulette activity 

def roulette(player_id):
    casino_lock.acquire()
    global casino_balance

    
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
        time.sleep(.5)

        print(f"Player {player_id} results: Net worth: ${total_winnings}, Balance of the casino: ${casino_balance}")
    casino_lock.release()

# Player threads
player_threads = []
for i in range(num_players):
    player_thread = threading.Thread(target=roulette, args=(i,))
    player_threads.append(player_thread)

# Start player threads
for thread in player_threads:
    thread.start()

# Wait for all player threads to finish
for thread in player_threads:
    thread.join()

# Final casino balance
print(f"Final Casino Balance: ${casino_balance}")
