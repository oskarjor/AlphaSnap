import random

from CONSTANTS import CARD_DICT, DECKSIZE

from Card import Card
from Location import Location
from Deck import Deck
import Hand

class Player(object):
    
    def __init__(self, cardNames: list[str], playerIdx: int, availableEnergy: int = 0) -> None:
        self.cardNames = cardNames
        self.deck = Deck(cardNames)
        self.hand = Hand.Hand()
        self.isStarting = None
        self.availableEnergy = availableEnergy
        self.playerIdx = playerIdx

    def __str__(self) -> str:
        return str(self.playerIdx)

    def playIsLegal(self, card: Card, location: Location) -> bool:
        if(not location.getPlayable(playerIdx=self.playerIdx)):
            return False
        if(card.cost > self.availableEnergy):
            return False
        return True
    
    def selectMove(self, legalMoves: list[list[Card, Location]]) -> list[Card, Location]:
        move = random.choice(legalMoves)
        return move

    def drawCard(self):
        if(self.hand.handIsFull()):
            return False
        self.hand.addCard(self.deck.removeCard())
        return True
    
    def playMove(self, legalMoves: list[list[Card, Location]]) -> bool:
        move = self.selectMove(legalMoves)
        if(move == None):
            return None
        card, location = move
        if(not self.playIsLegal(card, location)): # technically reduntant
            return None
        location.addCard(card, self)
        self.hand.removeCard(card)
        self.availableEnergy -= card.cost
        return move
        