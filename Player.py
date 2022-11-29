from __future__ import annotations

import random
from typing import TYPE_CHECKING

import Deck
import Hand

if TYPE_CHECKING:
    import Location
    import Card

class Player(object):
    
    def __init__(self, cardNames: list[str], playerIdx: int, availableEnergy: int = 0) -> None:
        self.cardNames = cardNames
        self.deck = Deck.Deck(cardNames)
        self.hand = Hand.Hand()
        self.isStarting = None
        self.availableEnergy = availableEnergy
        self.playerIdx = playerIdx

    def __str__(self) -> str:
        return str(self.playerIdx)

    def playIsLegal(self, card: Card.Card, location: Location.Location) -> bool:
        if(not location.getPlayable(playerIdx=self.playerIdx)):
            return False
        if(card.cost > self.availableEnergy):
            return False
        return True
    
    def selectMove(self, legalMoves: list[list[Card.Card, Location.Location]]) -> list[Card.Card, Location.Location]:
        move = random.choice(legalMoves)
        return move

    def drawCard(self):
        if(self.hand.handIsFull()):
            return False
        if(self.deck.deckIsEmpty()):
            return False
        self.hand.addCard(self.deck.removeCardByIndex())
        return True
    
    def playMove(self, move: list[Card.Card, Location.Location]):
        if(move == None):
            return None
        card, location = move
        if(not self.playIsLegal(card, location)): # technically reduntant
            return None
        location.addCard(card, self)
        self.hand.removeCard(card)
        self.availableEnergy -= card.cost
        return move
        