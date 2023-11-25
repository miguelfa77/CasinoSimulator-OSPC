import threading
import random
import time
import random

class Deck:
    """
    :subclasses: NormalDeck, BlackjackDeck
    :methods: shuffle_deck, draw_card
    """
    deck = []
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def draw_card(self):
        return self.deck.pop()

class NormalDeck(Deck):
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Spades']
        self.ranks = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        self.deck = [f'{rank} of {suit}' for suit in self.suits for rank in self.ranks]
    
class BlackJackDeck(Deck):
    def __init__(self):
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4

def deck_type(deck_type = None):
    """
    Factory Method
    :params: 'Normal','Blackjack'
    :returns: instance of a class
    """
    deck = {'Normal': NormalDeck,
            'Blackjack': BlackJackDeck}
    
    return deck[deck_type]()
