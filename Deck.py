from CONSTANTS import CARD_DICT

class Deck(object):
    def __init__(self, cardNames: list[str]) -> None:
        if(len(cardNames) != len(set(cardNames))):
            raise ValueError("Duplicate cards not allowed")
        for cardName in cardNames:
            if(cardName not in CARD_DICT.keys()):
                raise ValueError("Invalid card name")
        self.cards = [CARD_DICT[cardName]() for cardName in cardNames]
    
    def __str__(self) -> str:
        return [str(card) for card in self.cards]

if __name__ == "__main__":
    cardNamesLegal = ["mistyKnight", "abomination"]
    cardNamesDuplicate = ["mistyKnight", "mistyKnight"]
    cardNamesNonExisting = ["xxxxxxx"]
    deckLegal = Deck(cardNamesLegal)
    deckDuplicate = Deck(cardNamesDuplicate)
    deckNonExisting = Deck(cardNamesNonExisting)