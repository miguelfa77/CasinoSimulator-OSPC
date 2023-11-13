import random
import threading
import time 
from casino_class import Casino
from dealer_class import Dealer
from customer_classes import Customer
from deck_class import NormalDeck, BlackJackDeck
from typing import Optional

num_players = random.randrange(1, 5)
casino_balance = 100000

class Table(Casino):
    def __init__(self):
        super().__init__(self) # attr: balance, dealer_id
        self.current_bets = dict()   # dict holding total table bet amounts. specifies per player id.
        self.current_dealer: Optional[Dealer] = None
        self.current_players: Optional[Customer] = []
        self.dealer = {'lock': threading.Lock(), 'queue': []}
        self.customer = {'lock': threading.Lock(), 'queue': []}
        self.max_players = None

    def dealer_waiting(self):
        if self.dealer['queue']:
            return True
        return False

    def select_dealer(self):
        with self.dealer['lock']:
            self.current_dealer = self.dealer['queue'].pop()
    
    def customer_waiting(self):
        if self.customer['queue']:
            return True
        return False
    
    def select_customer(self):
        with self.customer['lock']:
            self.current_players.append(self.customer['queue'].pop())

class Roulette(Table):
    def __init__(self, balance, id):
        super().__init__(balance)
        self.table_id = id
        self.num_bets = random.randint(1, 12)
        # self.max_players = 10

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
    def __init__(self, balance, id):
        super().__init__(balance)
        self.table_id = id
        self.num_decks = random.randint(1, 8)
        # self.max_players = 3

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


class Poker(Table): # IMPLEMENTATION NOT FINAL
    """
    :methods: get_bets, play, payoff_bets, run
    :params: id, deck : NormalDeck

    """
    def __init__(self, id, deck : NormalDeck):
        super().__init__(self)
        self.table_id = id
        self.deck = deck
        self.max_players = 6
    
    def get_bets(self):
        for player_id in self.current_players:
            self.current_bets[player_id] = player_id.bet()      # bet method should return an int/float
        time.sleep(2)

    def play(self):  
        self.current_dealer.shuffle_deck()
        
        for player_id in self.current_players:
            hand = [self.current_dealer.draw_card(), self.current_dealer.draw_card()]

        board = []
        time.sleep(2)
        board.append(self.current_dealer.draw_card() for _ in range(3)) # FLOP
        time.sleep(2)
        board.append(self.current_dealer.draw_card())                   # TURN
        time.sleep(2)
        board.append(self.current_dealer.draw_card())                   # RIVER
    
    def payoff_bets(self):
        pot = sum(self.current_bets.values())
        payoff = pot * 0.98
        winner = random.choice(self.current_players)

        self.update_balance(amount=(pot - payoff))                      # RAKE aka what the casino keeps

        self.current_bets = {key: None for key in self.current_bets}   # EMPTY POT
        time.sleep(2)
        

    def run(self):
        while self.is_open:
            try:
                while not self.current_dealer or len(self.current_players) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_players) < 1 and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)

                with self.customer['lock'], self.dealer['lock']:
                    self.get_bets()
                    self.play()
                    self.payoff_bets()
            
            except Exception as e:
                print(f'Error-{e} in {self.table_id}: Selecting dealer and players again!')
                time.sleep(5)