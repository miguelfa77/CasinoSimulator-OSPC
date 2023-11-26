import random
import threading
import time 
from deck_class import deck_type

num_players = random.randrange(1, 5)
casino_balance = 100000

class Table():
    def __init__(self, casino:object):
        # self.log_file = 'tables_log.txt'
        self.current_bets = dict()   # dict holding total table bet amounts. specifies per player id.
        self.current_dealer = None
        self.current_players = []
        self.dealer = {'lock': threading.Lock(), 'queue': []}
        self.customer = {'lock': threading.Lock(), 'queue': []}
        self.max_players = None
        self.casino: object = casino

    def dealer_waiting(self):
        with self.dealer['lock']:
            if self.dealer['queue']:
                return True
            return False

    def select_dealer(self):
        with self.dealer['lock']:
            self.current_dealer = self.dealer['queue'].pop()
            return self.current_dealer
    
    def customer_waiting(self):
        with self.customer['lock']:
            if self.customer['queue']:
                return True
            return False
    
    def select_customer(self):
        with self.customer['lock']:
            self.current_players.append(self.customer['queue'].pop())
            return self.current_players

class Roulette(Table):
    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.num_bets = random.randint(1, 12)
        # self.max_players = 10
        self.casino = casino

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

            print(f"Player {player_id} results: Net worth: ${total_winnings}, Balance of the casino: ${self.casino.balance}")


class Blackjack(Table):
    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.num_decks = random.randint(1, 8)
        self.max_players = 3
        self.casino = casino

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
                    self.casino.balance -= winnings
                    total_winnings += winnings
                    print(f"Player {player_id} wins ${winnings} with a Blackjack!")
                else:
                    while sum(dealer_hand) < 17:
                        dealer_hand.append(deck.pop())

                    if sum(dealer_hand) > 21:
                        winnings = balance
                        self.casino.balance -= winnings
                        total_winnings += winnings
                        print(f"Player {player_id} wins ${winnings}! Dealer busts with {dealer_hand}")
                    elif sum(dealer_hand) < sum(player_hand):
                        winnings = balance
                        self.casino.balance -= winnings
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
    :params: id

    """
    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.deck = deck_type('normal')
        self.max_players = 6
        self.casino = casino
    
    def get_bets(self):
        for player in self.current_players:
            self.current_bets[player.customer_id] = player.update_bankroll() 
        time.sleep(1)

    def play(self):  
        self.current_dealer.shuffle_deck()

        hands = {player.customer_id:[self.current_dealer.draw_card(), self.current_dealer.draw_card()] for player in self.current_players}

        board = []
        time.sleep(1)
        board.extend(self.current_dealer.draw_card() for _ in range(3)) # FLOP
        time.sleep(1)
        board.append(self.current_dealer.draw_card())                   # TURN
        time.sleep(1)
        board.append(self.current_dealer.draw_card())                   # RIVER
    
    def payoff_bets(self):
        pot = sum(self.current_bets.values())
        payoff = pot * 0.98
        rake = pot - payoff
        winner = random.choice(self.current_players)

        self.casino.update_balance(amount=rake)                         # RAKE aka what the casino keeps

        self.current_bets = {}                                          # EMPTY POT
        time.sleep(1)
        

    def run(self):
        while self.casino.is_open:
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
                print(f'Error-{e} in table {self.table_id}: Selecting dealer and players again!')
                time.sleep(5)