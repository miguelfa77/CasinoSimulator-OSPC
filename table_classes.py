import random
import threading
import time 
from deck_class import deck_type

class Table():
    def __init__(self, casino:object):
        self.current_bets = dict()   # dict holding total table bet amounts. specifies per player id.
        self.current_dealer = None
        self.current_customers = []
        self.max_players = None
        self.casino: object = casino

    def dealer_waiting(self):
        with self.casino.locks['table']['dealer']:
            if self.casino.queues['table']['dealer']:
                return True
            return False

    def select_dealer(self):
        with self.casino.locks['table']['dealer']:
            self.current_dealer = self.casino.queues['table']['dealer'].pop()
            return self.current_dealer
    
    def customer_waiting(self):
        with self.casino.locks['table']['customer']:
            if self.casino.queues['table']['customer']:
                return True
            return False
    
    def select_customer(self):
        with self.casino.locks['table']['customer']:
            self.current_customers.append(self.casino.queues['table']['customer'].pop())
            return self.current_customers

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
        self.deck = deck_type('blackjack')
        self.max_players = 3
        self.casino = casino
    
    def get_bets(self):
        for customer in self.current_customers:
            bet = random.randrange(10,50)
            self.current_bets[customer] = bet
            customer.update_bankroll(-bet) 
        time.sleep(1)

    def run(self):
        while self.casino.is_open:
            try:
                while not self.current_dealer or len(self.current_customers) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_customers) < 1 and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)

                with self.casino.locks['table']['customer'], self.casino.locks['table']['dealer']:
                    self.get_bets()
                    self.play()
                    self.payoff_bets()
            except Exception as e:
                print(f'Error-{e} in table {self.table_id}: Selecting dealer and players again!')
                time.sleep(5)
            

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
        for customer in self.current_customers:
            bet = random.randrange(10,50)
            self.current_bets[customer] = bet
            customer.update_bankroll(-bet) 
        time.sleep(1)

    def play(self):  
        self.current_dealer.shuffle_deck()

        hands = {customer:[self.current_dealer.draw_card(), self.current_dealer.draw_card()] for customer in self.current_customers}

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
        winner = random.choice(self.current_customers)

        self.casino.update_balance(amount=rake, executor=Table)                         # RAKE aka what the casino keeps

        self.current_bets = {}                                          # EMPTY POT
        time.sleep(1)
        
    def run(self):
        while self.casino.is_open:
            try:
                while not self.current_dealer or len(self.current_customers) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_customers) < 1 and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)

                with self.casino.locks['table']['customer'], self.casino.locks['table']['dealer']:
                    self.get_bets()
                    self.play()
                    self.payoff_bets()
            
            except Exception as e:
                print(f'Error-{e} in table {self.table_id}: Selecting dealer and players again!')
                time.sleep(5)