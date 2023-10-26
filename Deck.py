from __future__ import annotations

import random
from typing import TYPE_CHECKING

import Card


class Deck(object):
    def __init__(self, cardNames: list[str]) -> None:
        if (len(cardNames) != len(set(cardNames))):
            raise ValueError("Duplicate cards not allowed")
        FLAT_CARD_DICT = Card.getFlatCardDict()
        for cardName in cardNames:
            if (cardName not in FLAT_CARD_DICT.keys()):
                raise ValueError("Invalid card name:", cardName)
        self.cards = [FLAT_CARD_DICT[cardName]() for cardName in cardNames]

    def __str__(self) -> str:
        return str([str(card) for card in self.cards])

    def getNumCards(self):
        return len(self.cards)

    def addCard(self, card: Card.Card):
        self.cards.append(card)

    def deckIsEmpty(self):
        return self.getNumCards() == 0

    def removeCard(self, targetCard: Card.Card):
        for i, card in enumerate(self.cards):
            if card == targetCard:
                return self.removeCardByIndex(i)

    def removeCardByIndex(self, index=0):
        if (self.deckIsEmpty()):
            raise IndexError("Deck is empty")
        if (index >= len(self.cards)):
            raise IndexError("Index out of range")
        return self.cards.pop(index)

    def shuffle(self):
        random.shuffle(self.cards)
