from __future__ import annotations

from typing import TYPE_CHECKING
import random
from utils.utils import all_subclasses
from GameHistory import gameHistory
from utils import GLOBAL_CONSTANTS

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

        # CARD ACTIONS:
        # eventType = cardPlayed                ->      turn : ["cardPlayed", player, card, location]       (check)
        # eventType = cardRevealed              ->      turn : ["cardRevealed", player, card, location]     (check)
        # eventType = cardMoved                 ->      turn : ["cardMoved", player, card, fromLocation, toLocation]
        # eventType = cardDestroyed             ->      turn : ["cardDestroyed", player, card, location]
        # eventType = cardDiscarded             ->      turn : ["cardDiscarded", player, card, location]
        #
        self.gameHistory = gameHistory

    def __str__(self) -> str:
        return f"{self.name} (C: {self.cost}, P: {self.getPower()})"

    def getPower(self):
        return self.power + sum(self.otherPowerSources.values())

    def ongoing(self, game: Game.Game):
        return None

    def onReveal(self, game: Game.Game):
        event = GLOBAL_CONSTANTS.CARD_REVEALED(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        self.revealed = True
        return None

    def onDestroy(self, game: Game.Game):
        event = GLOBAL_CONSTANTS.CARD_DESTROYED(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        return None

    def onMove(self, game: Game.Game, toLocation):
        event = GLOBAL_CONSTANTS.CARD_MOVED(
            player=self.player, card=self, fromLocation=self.atLocation, toLocation=toLocation)
        gameHistory.addEvent(event=event)
        self.atLocation = toLocation
        return None

    def onDiscard(self, game: Game.Game):
        event = GLOBAL_CONSTANTS.CARD_DISCARDED(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        return None

    def summon(self, game: Game.Game):
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
        super().onReveal(game=game)
        if (self.atLocation.cardPlayedThisTurn[1 - self.player.playerIdx]):
            self.predFunc(*self.args)


class PredictCardPowerGain(Card):

    def __init__(self, cost, power, name, predPowerGain):
        self.predPowerGain = predPowerGain
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
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
        super().onReveal(game=game)
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
        super().ongoing(game=game)
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
        super().onReveal(game=game)
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
        super().onReveal(game=game)
        FLAT_CARD_DICT = getFlatCardDict()
        randomCard = random.choice(list(FLAT_CARD_DICT.values()))()
        self.player.hand.addCard(randomCard)


class Blade(Card):

    def __init__(self, cost=1, power=3, name="Blade"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        randomCardInHand = self.player.hand.getRandomCard()
        self.player.hand.discardCard(randomCardInHand)


class Deadpool(Card):

    def __init__(self, cost=1, power=1, name="Deadpool"):
        super().__init__(cost, power, name)

    def onDestroy(self, game: Game.Game):
        super().onDestroy(game=game)
        currentPower = self.getPower()
        self.player.hand.addCard(Deadpool(power=currentPower * 2))


class HumanTorch(Card):

    def __init__(self, cost=1, power=2, name="Human Torch"):
        super().__init__(cost, power, name)

    def onMove(self, game: Game.Game, toLocation):
        super().onMove(game=game, toLocation=toLocation)
        self.power = self.power * 2


class Iceman(Card):

    def __init__(self, cost=1, power=2, name="Iceman"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        target_hand = game.getPlayerByIdx(1 - self.player.playerIdx).hand
        target_hand[random.randint(0, target_hand.getNumCards() - 1)].cost += 1


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


# class AbsorbingMan(Card):

#     def __init__(self, cost=4, power=4, name="Absorbing Man"):
#         super().__init__(cost, power, name)

#     def onReveal(self, game: Game.Game = None):
#         return super().onReveal(game)

#     # TODO: check if last card has onReveal function
#     # if yes -> this will copy it
#     def lastCardPlayed(self, game: Game.Game = None):
#         for t in range(game.turn, -1, -1):
#             for event in game.gameHistory[t]:
#                 pass


class AdamWarlock(Card):

    def __init__(self, cost=2, power=0, name="Adam Warlock"):
        super().__init__(cost, power, name)

    def ongoing(self, game: Game.Game):
        super().ongoing(game=game)
        if self.atLocation.playerIsWinning(self.player) == 1:
            self.player.drawCard()


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
