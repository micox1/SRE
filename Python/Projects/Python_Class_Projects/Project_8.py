'''
We're building a digital card system for an internal game platform. 
You'll be responsible for delivering two classes — Card and Deck — that will 
serve as the foundation for multiple card games down the line, so the code 
needs to be clean, reusable, and defensively written.

Card represents a single playing card. It needs to know its own suit and 
rank, be able to validate them, and expose some derived information about itself.

Deck manages a full collection of cards. It needs to handle all the operations 
a dealer would — building the deck, shuffling it, drawing from it, and resetting 
it when the game is over. 

A special configuration should also be supported for 
games that require two decks combined into one.
Use the random module for shuffling. No hardcoding cards — the deck should build 
itself dynamically from whatever Card tells it is valid. Make sure drawing from 
an empty deck doesn't crash the program. Every class should be able to stand on 
its own and be tested independently.
Deliver clean, working code. Be prepared to walk through any decision you made.
'''
import random as random

class Card:
    def __init__(self, suit, rank,):
        #Why "not in" and not != ?
        '''
        != is checking if the suit "heart" does not equal the entire list. This will always be True so it doesnt work. 
        It is not checking if it is not in the list but if it is the list itself. 
        "not in" is checking membership within the list
        '''
        for items in rank:
            if type(items) == str:
                items.lower()
        self.suit = suit.lower()
        self.rank = rank
    
    

    
    @staticmethod
    def rank_valid(ranks):
        rank = [2,3,4,5,6,7,8,9,"jack", "queen", "king", "ace"]
        if ranks not in rank:
            raise ValueError ("Not correct rank")
    
    @staticmethod
    def suit_valid(suits):
        suit = ["heart", "diamond", "club", "spade"]
        if suits not in suit:
            raise ValueError ("Not correct suit")
        
    @property
    def face_card(self):
        if self.rank == "king":
            return True 
        elif self.rank == "queen":
            return True
        elif self.rank == "jack":
            return True 
        else:
            return False
        
        

        
    def __str__(self):
        return f'Your suit is {self.suit} and rank is {self.rank}'
    
class Deck:
    def __init__(self):
        self.empty_deck = []

    @staticmethod
    def deck_valid(self):
        if len(self.empty_deck) != 52:
            raise ValueError ("Deck can only have 52 cards") 
        
    def add_rank(self, d_rank):
        if d_rank.rank_valid(d_rank.ranks) == True:
            self.empty_deck.append(d_rank)
    def add_suit(self, d_suit):
        if d_suit.rank_valid(d_suit.suits) == True:
            self.empty_deck.append(d_suit)
    
    def create_deck(self):
        suits = ["heart", "diamond", "club", "spade"]
        ranks = [2,3,4,5,6,7,8,9,"jack","queen","king","ace"]
        for suit in suits:
            for rank in ranks:
                self.empty_deck.append(Card(suit, rank))

    
   # Have to use random here      
    def shuffle_deck(self):
        random.shuffle(self.empty_deck)

    def drawing_card(self):
        if len(self.empty_deck) >= 1:
            return self.empty_deck.pop()
        else:
            raise ValueError( "No cards in deck" )
        
    def resetting_deck(self):
        self.empty_deck = []
        self.create_deck()