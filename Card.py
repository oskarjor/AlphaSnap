import random

class Card(object):

    def __init__(self, cost, power, name):
        self.name = name
        self.cost = cost
        self.power = power
        self.atLocation = None
        self.playerIdx = None
        self.ongoingTriggered = False
        self.revealed = False

    def __str__(self) -> str:
        return f"{self.name} (cost: {self.cost}, power: {self.power})"

    def ongoing(self):
        return None

    def onReveal(self):
        self.revealed = True
        return None

    def onDestroy(self):
        return None

    def onMove(self):
        return None

    def summon(self):
        return None


### Abstract (but slightly more specialized) classes
#
#

class PredictCard(Card):

    def __init__(self, cost, power, name, predPowerGain):
        self.predPowerGain = predPowerGain
        super().__init__(cost, power, name)

    def onReveal(self):
        self.revealed = True
        if(self.atLocation.cardPlayedThisTurn[1 - self.playerIdx]):
            self.power += self.predPowerGain

### 0-cost cards
#
#

class Wasp(Card):

    def __init__(self, cost=0, power=1, name="Wasp"):
        super().__init__(cost, power, name)

class Yellowjacket(Card):

    def __init__(self, cost=0, power=2, name="Yellowjacket"):
        super().__init__(cost, power, name)

### 1-cost cards
#
#

class MistyKnight(Card):
    
    def __init__(self, cost=1, power=2, name="Misty Knight"):
        super().__init__(cost, power, name)
        

class AntMan(Card):

    def __init__(self, cost=1, power=1, name="Ant-Man"):
        super().__init__(cost, power, name)

    def ongoing(self):
        locationFull = len(self.atLocation.cards[self.playerIdx]) == 4

        # trigger ongoing if location is full
        if(locationFull and not self.ongoingTriggered):
            self.ongoingTriggered = True
            self.power += 3
        
        # remove ongoing effect if it was active and the location is no longer full
        if(not locationFull and self.ongoingTriggered):
            self.ongoingTriggered = False
            self.power -= 3


class Elektra(Card):

    def __init__(self, cost=1, power=1, name="Elektra"):
        super().__init__(cost, power, name)

    def onReveal(self):
        self.revealed = True
        opposingOneCostCards = []
        for card in self.atLocation.getRevealedCards(1 - self.playerIdx):
            if card.cost == 1:
                opposingOneCostCards.append(card)
        
        if(len(opposingOneCostCards) == 0):
            return None
        
        cardToRemove = random.choice(opposingOneCostCards)
        self.atLocation.removeCard(cardToRemove, 1 - self.playerIdx)
        return cardToRemove


### 2-cost cards
#
#

class Shocker(Card):

    def __init__(self, cost=2, power=3, name="Shocker"):
        super().__init__(cost, power, name)


class StarLord(PredictCard):

    def __init__(self, cost=2, power=2, name="Star Lord", predPowerGain=3):
        super().__init__(cost, power, name, predPowerGain)


### 3-cost cards
#
#

class Cyclops(Card):

    def __init__(self, cost=3, power=4, name="Cyclops"):
        super().__init__(cost, power, name)

class Groot(PredictCard):

    def __init__(self, cost=3, power=3, name="Groot", predPowerGain=3):
        super().__init__(cost, power, name, predPowerGain)


### 4-cost cards
#
#

class Abomination(Card):

    def __init__(self, cost=4, power=6, name="Abomination"):
        super().__init__(cost, power, name)