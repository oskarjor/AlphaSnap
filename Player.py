import random

from CONSTANTS import CARD_DICT, DECKSIZE

from Card import Card
from Location import Location
from Deck import Deck

class Player(object):
    
    def __init__(self, cardNames: list[str], playerIdx: int, availableEnergy: int = 0) -> None:
        self.cardNames = cardNames
        self.deck = Deck(cardNames)
        self.hand = []
        self.isStarting = None
        self.availableEnergy = availableEnergy
        self.playerIdx = playerIdx

    def __str__(self) -> str:
        return str(self.playerIdx)

    def playIsLegal(self, card: Card, location: Location) -> bool:
        if(not location.isPlayable(playerIdx=self.playerIdx)):
            #print("The location is full or obstructed")
            return False
        if(card.cost > self.availableEnergy):
            #print(f"You don't have enough energy to play this card ({card})")
            return False
        return True
    
    def selectMove(self, legalMoves: list[list[Card, Location]]) -> list[Card, Location]:
        move = random.choice(legalMoves)
        return move

    def drawCard(self):
        self.hand.append(self.deck.pop(0))
    
    def playMove(self, legalMoves: list[list[Card, Location]]) -> bool:
        move = self.selectMove(legalMoves)
        if(move == None):
            return None
        card, location = move
        if(not self.playIsLegal(card, location)):
            print("This play is illegal")
        location.addCard(card, self)
        self.availableEnergy -= card.cost
        return move
        