from __future__ import annotations

import random
from typing import TYPE_CHECKING

from marvelsnap import Deck, Event, Hand
from marvelsnap.GameHistory import gameHistory

if TYPE_CHECKING:
    import Location
    import Card


class Player(object):

    def __init__(self, cards: list[Card.Card], playerIdx: int, availableEnergy: int = 0) -> None:
        self.deck = Deck.Deck(cards)
        self.hand = Hand.Hand()
        self.isStarting = None
        self.availableEnergy = availableEnergy
        self.playerIdx = playerIdx

    def __str__(self) -> str:
        return str(self.playerIdx)

    def playIsLegal(self, card: Card.Card, location: Location.Location) -> bool:
        if (not location.getPlayable(playerIdx=self.playerIdx)):
            return False
        if (card.cost > self.availableEnergy):
            return False
        return True

    def selectMove(self, legalMoves: list[list[Card.Card, Location.Location]]) -> list[Card.Card, Location.Location]:
        # TODO: implement a reinforcement agent, train it to become the best player
        # release it online and spread terror in the Marvel Snap community
        move = random.choice(legalMoves)
        return move

    def drawCard(self):
        if (self.hand.handIsFull()):
            return False
        if (self.deck.isEmpty()):
            return False
        cardToAdd = self.deck.removeCardByIndex()
        self.hand.addCard(cardToAdd)
        event = Event.PlayerDrawCard(player=self, card=cardToAdd)
        gameHistory.addEvent(event=event)
        return True

    def playMove(self, move: list[Card.Card, Location.Location]):
        if (move == None):
            raise TypeError("Move cannot be None")
        card, location = move
        if (not self.playIsLegal(card, location)):  # technically reduntant
            return None
        removed = self.hand.removeCard(card)
        if removed:
            location.addCard(card, self)
            self.availableEnergy -= card.cost
            return move
        return None
