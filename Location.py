from Card import Card

class Location(object):

    def __init__(self, name: str, idx: int, cardSpaces: list[int, int], desc: str) -> None:
        self.name = name
        self.idx = idx
        self.cardSpaces = cardSpaces
        self.cards = [[], []]
        self.desc = desc
        self.ongoinEnabled = True
        self.onRevealEnabled = True
        self.cardPlayedThisTurn = [False, False]

    def __str__(self) -> str:
        return f"{self.name} ({self.idx})"
    
    def addCard(self, card: Card, playerIdx: int):
        if(not self.getPlayable(playerIdx=playerIdx)):
            raise ValueError("Can't add more cards here")
        self.cards[playerIdx].append(card)
        card.atLocation = self
        card.playerIdx = playerIdx
        self.cardPlayedThisTurn[playerIdx] = True

    def triggerAllOngoing(self, playerIdx: int):
        if(self.ongoinEnabled):
            for card in self.cards[playerIdx]:
                card.ongoing()


    def triggerOnReveal(self, card: Card):
        if(self.onRevealEnabled):
            return card.onReveal()


    def removeCard(self, card: Card, playerIdx: int):
        self.cards[playerIdx].remove(card)
        self.triggerAllOngoing(playerIdx)
    
    def getTotalPower(self, playerIdx: int):
        return sum([card.power for card in self.cards[playerIdx]])

    def getCards(self, playerIdx: int):
        return self.cards[playerIdx]

    def getRevealedCards(self, playerIdx: int):
        return [card for card in self.cards[playerIdx] if card.revealed]

    def getAmountOfCards(self, playerIdx: int):
        return len(self.cards[playerIdx])

    def getPlayable(self, playerIdx: int):
        if self.getAmountOfCards(playerIdx) < self.cardSpaces[playerIdx]:
            return True
        return False

class RuinsLocation(Location):

    def __init__(self, idx: int):
        super(RuinsLocation, self).__init__(name="Ruins", idx=idx, cardSpaces=[4, 4], desc="A ruined land")
