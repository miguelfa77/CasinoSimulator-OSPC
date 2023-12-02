import random
import threading
import time 
from casino_class import Casino
from dealer_class import Dealer
from customer_classes import Customer
from deck_class import NormalDeck, BlackJackDeck
from typing import Optional



class Table():
    def __init__(self, casino, table_id, game_type, capacity, number_dealer, minimum_bet):
        self.table_id = table_id  
        self.casino = casino
        self.game_type = game_type  
        self.table_capacity = capacity 
        self.max_number_dealer = number_dealer 
        self.minimum_bet = minimum_bet  
        
        
        self.list_current_dealers: Optional[Dealer] = None 
        self.list_current_players[game_type]: Optional[Customer] = [] 

    
        self.dealers_waiting_to_work = {'lock': threading.Lock(), 'queue': []} 
        self.customer_waiting_to_play = {'lock': threading.Lock(), 'queue': []} 

        self.list_current_players = {"queue":list(), "lock":threading.Lock()}
        self.list_current_dealers = {"queue":list(), "lock":threading.Lock()}

    def select_next_dealer_to_work(self):
        if len(self.dealers_waiting_to_work['queue']) > 0:
            with self.dealers_waiting_to_work['lock']:
                next_dealer = self.dealers_waiting_to_work['queue'].pop(0)
                return next_dealer
        else:
            return "No dealers"
    
    def add_dealer_to_table(self):
        with self.list_current_dealers['lock']:
            if len(self.list_current_dealers['queue']) < self.max_number_dealer:
                next_dealer = self.select_next_dealer_to_work()
                if next_dealer != "No dealers":
                    self.list_current_dealers['queue'].append(next_dealer)
                else:
                    print("There are no dealers waiting to work.")
            else:
                print("There the table is already at max capacity of dealer(s).")
        
    def select_next_customer_to_play(self):
        if len(self.customer_waiting_to_play['queue']) > 0:
            with self.customer_waiting_to_play['lock']:
                next_customer = self.customer_waiting_to_play['queue'].pop(0)
                return next_customer
        else:
            return "No customers"
    
    def add_customer_to_table(self):
        with self.list_current_players['lock']:
            if len(self.list_current_players['queue']) < self.table_capacity:
                next_player = self.select_next_customer_to_play()
                if next_player != "No customers":
                    self.list_current_players['queue'].append(next_player)
                else:
                    print("There are no players waiting to play.")
            else:
                print("There the table is already at max capacity of players.")

class Roulette(Table):
    def __init__(self, table_id, casino, game_type, capacity, number_dealer, minimum_bet):
        super().__init__(table_id, casino, game_type, capacity, number_dealer, minimum_bet)

    def play(self):
        with self.list_current_players['lock']:
            for current_player in self.list_current_players['queue']:
                bet_amount = random.randrange(self.minimum_bet, 1000)
                number_bet_by_player = random.randint(0, 37)
                winning_number = random.randint(0, 37)

                print(f"Player {current_player.customer_id} bets ${bet_amount} on number {number_bet_by_player}. The winning number was {winning_number}.")

                if winning_number == number_bet_by_player:
                    winnings = bet_amount * 3
                    with self.casino.locks['balance']:
                        self.casino._balance -= (winnings - bet_amount) 
                    current_player.bankroll += winnings - bet_amount 
                    print(f"Player {current_player.customer_id} wins ${winnings} on number {number_bet_by_player}!")
                else:
                    with self.casino.locks['balance']:
                        self.casino._balance += bet_amount # Casino gana dinero
                    current_player.bankroll -= bet_amount # Customer pierde dinero
                    print(f"Player {current_player.customer_id} loses ${bet_amount} on number {number_bet_by_player}!")

                print(f"Player {current_player.customer_id} results: Net worth: ${current_player.bankroll}, Balance of the casino: ${self.casino._balance}")

# self.decks = {'Normal_deck': NormalDeck(), 'BlackJack_deck': BlackJackDeck()}} # esto se tiene que añadir al class de casino

# class BlackJackDeck(Deck):
#    def __init__(self):
#        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,'A'] * 4
#    def convert_a(self, current_hand):
#        if "A" in current_hand:
#            current_hand.remove("A")
#            sum_of_current_hand = sum(current_hand)
#            if sum_of_current_hand + 11 > 21:
#                current_hand.append(1)
#            else:
#                current_hand.append(11)
#            return current_hand
#        else:
#            return "No A in hand"


class Blackjack(Table):
    def __init__(self, table_id, casino, game_type, capacity, number_dealer, minimum_bet):
        super().__init__(table_id, casino, game_type, capacity, number_dealer, minimum_bet)
        self.deck = self.casino.decks['BlackJack_deck'] 

    
    def play(self): 
        with self.list_current_players['lock']:
            self.deck.shuffle()
            dealer_hand = [self.deck.draw_card(), self.deck.draw_card()]
            while True:
                dealer_hand_after_a = self.deck.convert_a(dealer_hand)
                if dealer_hand_after_a == "No A in hand":
                    break
                else:
                    dealer_hand = dealer_hand_after_a


            if len(self.list_current_players['queue']) <= 7 and len(self.list_current_players['queue']) > 4:
                self.deck.deck = self.deck.deck * 2
            elif len(self.list_current_players['queue']) > 7:
                self.deck.deck = self.deck.deck * 4


            for current_player in self.list_current_players['queue']: # Simulates a game of bj for each player in the self.list_current_players list.
                player_hand = [self.deck.draw_card(), self.deck.draw_card()]
                bet_amount = random.randrange(self.minimum_bet, 1000)
                while True:
                    player_hand_after_a = self.deck.convert_a(player_hand)
                    if player_hand_after_a == "No A in hand":
                        break
                    else:
                        player_hand = player_hand_after_a
                
                if sum(player_hand) == 21:
                    winnings = bet_amount * 2
                    
                    with self.casino.locks['balance']:
                        self.casino._balance -= (winnings - bet_amount) # Casino pierde dinero
                    current_player.bankroll += winnings - bet_amount # Cliente gana dinero

                    print(f"Player {current_player.customer_id} wins ${winnings} with a Blackjack!")
                else:
                    while sum(dealer_hand) < 17:
                        dealer_hand.append(self.deck.draw_card())
                        while True:
                            dealer_hand_after_a = self.deck.convert_a(dealer_hand)
                            if dealer_hand_after_a == "No A in hand":
                                break
                            else:
                                dealer_hand = dealer_hand_after_a

                    if sum(dealer_hand) > 21:
                        winnings = bet_amount * 1.5
                        with self.casino.locks['balance']:
                            self.casino._balance -= (winnings - bet_amount)
                        current_player.bankroll += winnings - bet_amount

                        print(f"Player {current_player.customer_id} wins ${winnings}! Dealer busts with {sum(dealer_hand)}")
                    elif sum(dealer_hand) < sum(player_hand):
                        winnings = bet_amount * 1.5
                        with self.casino.locks['balance']:
                            self.casino._balance -= (winnings - bet_amount)
                        current_player.bankroll += winnings - bet_amount

                        print(f"Player {current_player.customer_id} wins ${winnings}! Dealer busts with {sum(dealer_hand)}")
                    elif sum(dealer_hand) > sum(player_hand):
                        current_player.bankroll -= bet_amount
                        with self.casino.locks['balance']:
                            self.casino._balance += bet_amount
                        print(f"Player {current_player.customer_id} loses ${bet_amount}! Player has {sum(player_hand)}, dealer has {sum(dealer_hand)}")
                    
                print(f"Player {current_player.customer_id} results: Net worth: ${current_player.bankroll}, Balance of the casino: ${self.casino._balance}")


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
        for player_id in self.list_current_players:
            self.current_bets[player_id] = random.randint(1,10)
        time.sleep(2)

    def play(self):  
        self.list_current_dealers.shuffle_deck()
        
        for player_id in self.list_current_players:
            hand = [self.list_current_dealers.draw_card(), self.list_current_dealers.draw_card()]

        board = []
        time.sleep(2)
        board.append(self.list_current_dealers.draw_card() for _ in range(3)) # FLOP
        time.sleep(2)
        board.append(self.list_current_dealers.draw_card())                   # TURN
        time.sleep(2)
        board.append(self.list_current_dealers.draw_card())                   # RIVER
    
    def payoff_bets(self):
        pot = sum(self.current_bets.values())
        payoff = pot * 0.98
        winner = random.choice(self.list_current_players)

        self.update_balance(amount=(pot - payoff))                      # RAKE aka what the casino keeps

        self.current_bets = {key: None for key in self.current_bets}   # EMPTY POT
        time.sleep(2)
        
    def run(self):
        while self.is_open:
            while not self.list_current_dealers:
                self.select_dealer()

            while len(self.list_current_players) < self.max_players and self.customer['queue']:
                self.select_customer()

            while self.is_open:  # Run indefinitely until the gameplay loop succeeds
                try:
                    if not (self.list_current_dealers and self.list_current_players):
                        # Attempt to select dealer or customer again
                        while not self.list_current_dealers:
                            self.select_dealer()

                        while len(self.list_current_players) < self.max_players and self.customer['queue']:
                            self.select_customer()
                    else:
                        with self.customer['lock']:
                            with self.dealer['lock']:
                                self.get_bets()
                                self.play()
                                self.payoff_bets()
                except Exception as e:
                    print(f'Error-{e} in {self.table_id}: Selecting dealer and players again!')
                    time.sleep(5)
                






