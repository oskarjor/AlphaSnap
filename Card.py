from __future__ import annotations

from typing import TYPE_CHECKING
import random
from utils.utils import all_subclasses

if TYPE_CHECKING:
    import Game


class Card(object):

    def __init__(self, cost, power, name):
        self.name = name
        self.cost = cost
        self.power = power
        self.atLocation = None
        self.player = None
        self.revealed = False
        self.otherPowerSources = {}

    def __str__(self) -> str:
        return f"{self.name} (C: {self.cost}, P: {self.getPower()})"

    def getPower(self):
        return self.power + sum(self.otherPowerSources.values())

    def ongoing(self, game: Game.Game = None):
        return None

    def onReveal(self, game: Game.Game = None):
        self.revealed = True
        if game != None:
            game.addToPlayHistory(
                ["cardRevealed", self.player, self, self.atLocation])
        return None

    def onDestroy(self, game: Game.Game = None):
        if game != None:
            game.addToPlayHistory(
                ["cardDestroyed", self.player, self, self.atLocation])
        return None

    def onMove(self, game: Game.Game = None):
        return None

    def onDiscard(self, game: Game.Game = None):
        if game != None:
            game.addToPlayHistory(
                ["cardDiscarded", self.player, self, self.atLocation])
        return None

    def summon(self, game: Game.Game = None):
        return None


# Abstract (but slightly more specialized) classes
#
#

class PredictCard(Card):

    def __init__(self, cost, power, name, predFunc, *args):
        self.predFunc = predFunc
        self.args = args
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        if (self.atLocation.cardPlayedThisTurn[1 - self.player.playerIdx]):
            self.predFunc(*self.args)


class PredictCardPowerGain(Card):

    def __init__(self, cost, power, name, predPowerGain):
        self.predPowerGain = predPowerGain
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        self.revealed = True
        if (self.atLocation.cardPlayedThisTurn[1 - self.player.playerIdx]):
            self.power += self.predPowerGain

# implemented cards


class Wasp(Card):

    def __init__(self, cost=0, power=1, name="Wasp"):
        super().__init__(cost, power, name)


class Yellowjacket(Card):

    def __init__(self, cost=0, power=2, name="Yellowjacket"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        revealedCardsAtLocation = self.atLocation.getRevealedCards(
            self.player.playerIdx)
        for card in revealedCardsAtLocation:
            if card != self:
                card.power -= 1


class Mantis(PredictCard):

    def __init__(self, cost=1, power=2, name="Mantis", *args):
        super().__init__(cost, power, name, self.drawCard, *args)

    def drawCard(self):
        self.player.drawCard()


class MistyKnight(Card):

    def __init__(self, cost=1, power=2, name="Misty Knight"):
        super().__init__(cost, power, name)


class AntMan(Card):

    def __init__(self, cost=1, power=1, name="Ant-Man"):
        self.ongoingTriggered = False
        super().__init__(cost, power, name)

    def ongoing(self, game: Game.Game):
        super().ongoing(game)
        locationFull = len(self.atLocation.cards[self.player.playerIdx]) == 4

        # trigger ongoing if location is full
        if (locationFull and not self.ongoingTriggered):
            self.ongoingTriggered = True
            self.power += 3

        # remove ongoing effect if it was active and the location is no longer full
        if (not locationFull and self.ongoingTriggered):
            self.ongoingTriggered = False
            self.power -= 3


class Elektra(Card):

    def __init__(self, cost=1, power=1, name="Elektra"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        opposingOneCostCards = []
        for card in self.atLocation.getRevealedCards(1 - self.player.playerIdx):
            if card.cost == 1:
                opposingOneCostCards.append(card)

        if (len(opposingOneCostCards) == 0):
            return None

        cardToRemove = random.choice(opposingOneCostCards)
        self.atLocation.removeCard(cardToRemove, 1 - self.player.playerIdx)
        return cardToRemove


class Agent13(Card):

    def __init__(self, cost=1, power=2, name="Agent 13"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        FLAT_CARD_DICT = getFlatCardDict()
        randomCard = random.choice(list(FLAT_CARD_DICT.values()))()
        self.player.hand.addCard(randomCard)


class Blade(Card):

    def __init__(self, cost=1, power=3, name="Blade"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        randomCardInHand = self.player.hand.getRandomCard()
        self.player.hand.discardCard(randomCardInHand)


class Deadpool(Card):

    def __init__(self, cost=1, power=1, name="Deadpool"):
        super().__init__(cost, power, name)

    def onDestroy(self, game: Game.Game):
        super().onDestroy(game)
        currentPower = self.getPower()
        self.player.hand.addCard(Deadpool(power=currentPower * 2))


class HumanTorch(Card):

    def __init__(self, cost=1, power=2, name="Human Torch"):
        super().__init__(cost, power, name)

    def onMove(self, game: Game.Game):
        super().onMove(game)
        self.power = self.power * 2


class Iceman(Card):

    def __init__(self, cost=1, power=2, name="Iceman"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game)
        # TODO: increase cost of opponents card by 1


class Shocker(Card):

    def __init__(self, cost=2, power=3, name="Shocker"):
        super().__init__(cost, power, name)


class StarLord(PredictCardPowerGain):

    def __init__(self, cost=2, power=2, name="Star Lord", predPowerGain=3):
        super().__init__(cost, power, name, predPowerGain)


class Cyclops(Card):

    def __init__(self, cost=3, power=4, name="Cyclops"):
        super().__init__(cost, power, name)


class Groot(PredictCardPowerGain):

    def __init__(self, cost=3, power=3, name="Groot", predPowerGain=3):
        super().__init__(cost, power, name, predPowerGain)


class TheThing(Card):

    def __init__(self, cost=4, power=6, name="The Thing"):
        super().__init__(cost, power, name)


class Abomination(Card):

    def __init__(self, cost=5, power=9, name="Abomination"):
        super().__init__(cost, power, name)


class Hulk(Card):

    def __init__(self, cost=6, power=12, name="Hulk"):
        super().__init__(cost, power, name)


def getFlatCardDict():
    FLAT_CARD_DICT = {}
    sub = all_subclasses(Card)
    for s in sub:
        try:
            FLAT_CARD_DICT[s().name] = s
        except:
            pass
    return FLAT_CARD_DICT


if __name__ == "__main__":
    FCD = getFlatCardDict()
    print(FCD.keys())
