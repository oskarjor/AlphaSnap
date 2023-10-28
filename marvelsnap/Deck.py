import random

from marvelsnap import Card


class Deck(object):
    def __init__(self, cards: list[Card.Card]) -> None:
        cardNames = [card.name for card in cards]
        if (len(cardNames) != len(set(cardNames))):
            raise ValueError("Duplicate cards not allowed")
        self.cards = cards

    def createCardsFromCardNames(self, cardNames: list[str]) -> None:
        if (len(cardNames) != len(set(cardNames))):
            raise ValueError("Duplicate cards not allowed")
        FLAT_CARD_DICT = Card.getFlatCardDict()
        for cardName in cardNames:
            if (cardName not in FLAT_CARD_DICT):
                raise ValueError("Invalid card name:", cardName)
        self.cards = [FLAT_CARD_DICT[cardName]() for cardName in cardNames]

    def __str__(self) -> str:
        return str([str(card) for card in self.cards])

    def __len__(self) -> int:
        return len(self.cards)

    def getNumCards(self):
        return len(self.cards)

    def addCard(self, card: Card.Card):
        self.cards.append(card)

    def isEmpty(self):
        return self.getNumCards() == 0

    def removeCard(self, targetCard: Card.Card):
        for i, card in enumerate(self.cards):
            if card == targetCard:
                return self.removeCardByIndex(i)

    def removeCardByIndex(self, index=0):
        if (self.isEmpty()):
            raise IndexError("Deck is empty")
        if (index >= len(self.cards)):
            raise IndexError("Index out of range")
        return self.cards.pop(index)

    def shuffle(self):
        random.shuffle(self.cards)
