from CONSTANTS import FLAT_CARD_DICT
import random

class Deck(object):
    def __init__(self, cardNames: list[str]) -> None:
        if(len(cardNames) != len(set(cardNames))):
            raise ValueError("Duplicate cards not allowed")
        for cardName in cardNames:
            if(cardName not in FLAT_CARD_DICT.keys()):
                raise ValueError("Invalid card name")
        self.cards = [FLAT_CARD_DICT[cardName]() for cardName in cardNames]
    
    def __str__(self) -> str:
        return [str(card) for card in self.cards]

    def removeCard(self, index=0):
        if(len(self.cards) == 0):
            return
        return self.cards.pop(index)

    def shuffle(self):
        random.shuffle(self.cards)