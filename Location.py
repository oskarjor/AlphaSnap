from Card import Card
# import Player

class Location(object):

    def __init__(self, idx: int, name: str, cardSpaces: list[int, int], desc: str) -> None:
        self.name = name
        self.idx = idx
        self.cardSpaces = cardSpaces
        self.cards = [[], []]
        self.desc = desc
        self.ongoinEnabled = True
        self.onRevealEnabled = True
        self.cardPlayedThisTurn = [False, False]
        self.otherPowerSources = []

    def __str__(self) -> str:
        return f"{self.name} ({self.idx})"

    def locationAbility(self):
        return None
    
    def addCard(self, card: Card, player):
        playerIdx = player.playerIdx
        if(not self.getPlayable(playerIdx=playerIdx)):
            raise ValueError("Can't add more cards here")
        self.cards[playerIdx].append(card)
        card.atLocation = self
        card.player = player
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
        return sum([card.getPower() for card in self.getRevealedCards(playerIdx)])

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

class Ruins(Location):

    def __init__(self, idx, name= "Ruins", cardSpaces=[4, 4], desc="A ruined land") -> None:
        super().__init__(name, idx, cardSpaces, desc)

class Atlantis(Location):

    def __init__(self, idx, name="Atlantis", cardSpaces=[4, 4], desc="If you only have one card here, it has +5 Power") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self):
        for i in range(2):
            if(len(self.cards[i]) == 1):
                self.cards[i][0].otherPowerSources[self] = 5
            else:
                for card in self.cards[i]:
                    card.otherPowerSources.pop(self, None)
