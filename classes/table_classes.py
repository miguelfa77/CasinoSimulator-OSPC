import random
import time
import deck_class as dck


class Table:
    def __init__(self, casino: object):
        self.current_bets = {}  # dict holding total table bet amounts. specifies per player id.
        self.current_dealer = None
        self.current_customers = []
        self.max_players = None
        self.casino = casino

    def dealer_waiting(self):
        if self.casino.queues["table"]["dealer"]:
            return True
        return False

    def select_dealer(self):
        with self.casino.locks["table"]["dealer"]:
            self.current_dealer = self.casino.queues["table"]["dealer"].pop()
            return self.current_dealer

    def customer_waiting(self):
        if self.casino.queues["table"]["customer"]:
            return True
        return False

    def select_customer(self):
        with self.casino.locks["table"]["customer"]:
            self.current_customers.append(self.casino.queues["table"]["customer"].pop())
            return self.current_customers


class Roulette(Table):
    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.max_players = 10
        self.casino = casino
        self.nums_chosen = {}

    def get_bets(self):
        for customer in self.current_customers:
            bet = random.randrange(10, 100)
            self.current_bets[customer] = bet
            customer.bet(bet)
            time.sleep(0.5)
            self.nums_chosen[customer] = random.randrange(0, 36)
        self.current_bets[self] = random.randrange(10, 100)

    def clear_hands(self):
        self.current_bets.clear()

    def play(self):
        outcome = random.randrange(0, 36)
        for customer in self.current_customers:
            bet_amount = self.current_bets[customer]
            if self.nums_chosen[customer] == outcome:
                customer.win(outcome * 36)
                with self.casino.locks["balance"]:
                    self.casino._balance -= outcome * 36
            else:
                with self.casino.locks["balance"]:
                    self.casino._balance += bet_amount
        self.clear_hands()

    def run(self):
        while self.casino.is_open:
            try:
                while not self.current_dealer or len(self.current_customers) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_customers) < self.max_players and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)

                self.get_bets()
                self.play()
            except Exception as e:
                self.casino.LOG.error(f"Error: {e}", exc_info=True)
                time.sleep(5)


class BlackJack(Table):
    """
    :methods: clear_hands, get_bets, play, payoff_bets, run
    :params: table_id, deck, max_players, casino, _hands
    """

    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.deck = dck.deck_type("blackjack")
        self.max_players = 3
        self.casino = casino
        self._hands = {}

    def clear_hands(self):
        self._hands.clear()
        self.current_bets.clear()

    def get_bets(self):
        for customer in self.current_customers:
            bet = random.randint(100, 1000)
            self.current_bets[customer] = bet
            customer.bet(bet)
            time.sleep(0.5)
        self.current_bets[self] = random.randrange(10, 100)

    def payoff_bets(self):
        for player in self.current_customers:
            if sum(self._hands[player]) == 21:
                print(f"Player {player.name} has won.")
                player.win(sum(self.current_bets.values()))
            elif (sum(self._hands[player]) - 21) > (sum(self._hands[self]) - 21):
                player.win(sum(self.current_bets.values()))
            else:
                with self.casino.locks["balance"]:
                    self.casino._balance += sum(self.current_bets.values())

    def play(self):
        self.deck.shuffle_deck()
        for _ in range(2):
            for player in self.current_customers:
                self._hands[player] = (self.deck.deck.pop(), self.deck.deck.pop())
            self._hands[self] = (self.deck.deck.pop(), self.deck.deck.pop())
        self.payoff_bets()
        self.clear_hands()

    def run(self):
        while self.casino.is_open:
            try:
                while not self.current_dealer or len(self.current_customers) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_customers) < self.max_players and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)
                self.get_bets()
                self.play()
                self.payoff_bets()
            except Exception as e:
                self.casino.LOG.error(f"Error: {e}", exc_info=True)
                time.sleep(5)


class Poker(Table):
    """
    :methods: get_bets, play, payoff_bets, run
    :params: id

    """

    def __init__(self, id, casino):
        super().__init__(self)
        self.table_id = id
        self.deck = dck.deck_type("normal")
        self.max_players = 6
        self.casino = casino

    def get_bets(self):
        for customer in self.current_customers:
            bet = random.randrange(10, 50)
            self.current_bets[customer] = bet
            customer.bet(bet)
        time.sleep(1)

    def play(self):
        self.current_dealer.shuffle_deck()

        hands = {
            customer: [self.current_dealer.draw_card(), self.current_dealer.draw_card()]
            for customer in self.current_customers
        }

        board = []
        time.sleep(1)
        board.extend(self.current_dealer.draw_card() for _ in range(3))  # FLOP
        time.sleep(1)
        board.append(self.current_dealer.draw_card())  # TURN
        time.sleep(1)
        board.append(self.current_dealer.draw_card())  # RIVER

    def payoff_bets(self):
        pot = sum(self.current_bets.values())
        payoff = pot * 0.98
        rake = pot - payoff
        winner = random.choice(self.current_customers)

        self.casino.update_balance(amount=rake, executor=Table)  # RAKE aka what the casino keeps

        self.current_bets = {}  # EMPTY POT
        time.sleep(1)

    def run(self):
        while self.casino.is_open:
            try:
                while not self.current_dealer or len(self.current_customers) < 1:
                    if not self.current_dealer and self.dealer_waiting():
                        self.select_dealer()
                    elif len(self.current_customers) < self.max_players and self.customer_waiting():
                        self.select_customer()
                    else:
                        time.sleep(5)

                with self.casino.locks["table"]["customer"], self.casino.locks["table"]["dealer"]:
                    self.get_bets()
                    self.play()
                    self.payoff_bets()

            except Exception as e:
                self.casino.LOG.error(f"Error: {e}", exc_info=True)
                time.sleep(5)
