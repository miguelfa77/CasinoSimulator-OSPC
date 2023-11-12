import random
import threading 
from casino_class import Casino
from dealer_class import Dealer

num_players = random.randrange(1, 5)
casino_balance = 100000

class Table(Casino, Dealer):
    def _init_(self):
        Casino.__init__()
        Dealer.__init__()
        self.current_bets = {'bet_amount':dict()}   # dict holding total table bet amounts. specifies per player id.
        self.current_dealer = None
        self.current_players = []
        self.dealer = {'lock': threading.Lock(), 'queue': []}
        self.customer = {'lock': threading.Lock(), 'queue': []}

    def select_dealer(self):
        self.current_dealer = self.dealer['queue'].pop()

class Roulette(Table):
    def _init_(self, balance):
        super()._init_(balance)
        # self.max_players = 10
        self.num_bets = random.randint(1, 12)

    def play(self, player_id, balance):
        with self.lock:
            total_winnings = 0

            for _ in range(self.num_bets):
                bet_amount = random.randrange(10, 1000)
                number_bet = random.randrange(0, 36)
                outcome = random.randrange(0, 36)

                if outcome == number_bet:
                    winnings = bet_amount * 36
                    self.balance -= winnings
                    total_winnings += winnings
                    print(f"Player {player_id} wins ${winnings} on number {number_bet}!")
                else:
                    self.balance += bet_amount
                    total_winnings -= bet_amount
                    print(f"Player {player_id} loses ${bet_amount} on number {number_bet}!")

            print(f"Player {player_id} results: Net worth: ${total_winnings}, Balance of the casino: ${self.balance}")

class Blackjack(Table):
    def _init_(self, balance):
        super()._init_(balance)
        # self.max_players = 3
        self.num_decks = random.randint(1, 8)

    def play(self, player_id, balance):
        with self.lock:
            total_winnings = 0

            for _ in range(self.num_decks):
                deck = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4
                random.shuffle(deck)
                player_hand = [deck.pop(), deck.pop()]
                dealer_hand = [deck.pop(), deck.pop()]

                if sum(player_hand) == 21:
                    winnings = balance * 1.5
                    self.balance -= winnings
                    total_winnings += winnings
                    print(f"Player {player_id} wins ${winnings} with a Blackjack!")
                else:
                    while sum(dealer_hand) < 17:
                        dealer_hand.append(deck.pop())

                    if sum(dealer_hand) > 21:
                        winnings = balance
                        self.balance -= winnings
                        total_winnings += winnings
                        print(f"Player {player_id} wins ${winnings}! Dealer busts with {dealer_hand}")
                    elif sum(dealer_hand) < sum(player_hand):
                        winnings = balance
                        self.balance -= winnings
                        total_winnings += winnings
                        print(f"Player {player_id} wins ${winnings}! Player has {player_hand}, dealer has {dealer_hand}")
                    elif sum(dealer_hand) > sum(player_hand):
                        self.balance += balance
                        total_winnings -= balance
                        print(f"Player {player_id} loses ${balance}! Player has {player_hand}, dealer has {dealer_hand}")
                    else:
                        print(f"Player {player_id} pushes! Player has {player_hand}, dealer has {dealer_hand}")

            print(f"Player {player_id} results: Net worth: ${total_winnings}, Balance of the casino: ${self.balance}")

class Poker(Table):
    def __init__(self, balance):
        super().__init__()
        # self.max_players = 6
        



        
