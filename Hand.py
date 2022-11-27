import random
import Card

class Hand(object):
    def __init__(self) -> None:
        self.maxHandSize = 7
        self.cards = []
    
    def __str__(self) -> str:
        return [str(card) for card in self.cards]

    def handIsFull(self):
        if len(self.cards) >= self.maxHandSize:
            return True
        return False

    def addCard(self, card: Card.Card):
        if self.handIsFull():
            return False
        if card == None:
            return False
        self.cards.append(card)
        return True

    def removeCard(self, index=0):
        if(len(self.cards) == 0):
            return
        return self.cards.pop(index)