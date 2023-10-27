import random

from typing import TYPE_CHECKING
import Card


class Hand(object):
    def __init__(self, cards: list[Card.Card] = None) -> None:
        self.maxHandSize = 7
        if not cards:
            self.cards = []
        else:
            self.cards = cards

    def __str__(self) -> str:
        return str([str(card) for card in self.cards])

    def __len__(self) -> int:
        return len(self.cards)

    def getNumCards(self):
        return len(self.cards)

    def handIsFull(self):
        if self.getNumCards() >= self.maxHandSize:
            return True
        return False

    def addCard(self, card: Card.Card):
        if self.handIsFull():
            return False
        if card == None:
            return False
        self.cards.append(card)
        return True

    def getCards(self):
        return self.cards.copy()

    def getRandomCard(self) -> Card.Card | None:
        if len(self.cards) > 0:
            return random.choice(self.cards.copy())
        return None

    def discardCard(self, card: Card.Card) -> bool:
        if (self.removeCard(card=card)):
            card.onDiscard()
            return True
        return False

    def removeCard(self, card: Card.Card):
        if (len(self.cards) == 0 or card not in self.cards):
            return False
        self.cards.remove(card)
        return True
