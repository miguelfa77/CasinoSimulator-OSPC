import random

class Deck:
    deck = []

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()


class NormalDeck(Deck):
    def __init__(self):
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.deck = [f"{rank} of {suit}" for suit in self.suits for rank in self.ranks]


class BlackJackDeck(Deck):
    def __init__(self):
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4


def deck_type(deck_type) -> NormalDeck or BlackJackDeck:
    """
    Factory Method
    :params: 'normal','blackjack'
    :returns: instance of a class
    """
    deck = {"normal": NormalDeck, "blackjack": BlackJackDeck}

    return deck[deck_type]()