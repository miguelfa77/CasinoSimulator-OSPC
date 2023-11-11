import threading
import random
import time
import random

class Deck():
    def __init__(self) -> None:
        self.deck = []

    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def draw_card(self):
        return self.deck.pop()

class NormalDeck(Deck):
    def __init__(self) -> None:
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Spades']
        self.ranks = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        self.deck = [f'{rank} of {suit}' for suit in self.suits for rank in self.ranks]
    
class BlackJackDeck(Deck):
    def __init__(self) -> None:
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4