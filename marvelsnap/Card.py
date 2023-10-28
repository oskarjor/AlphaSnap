from __future__ import annotations

from typing import TYPE_CHECKING
import random
from utils.utils import all_subclasses
from GameHistory import gameHistory
from utils import GLOBAL_CONSTANTS
import Event

if TYPE_CHECKING:
    import Game
    import Player
    import Location


class Card(object):

    def __init__(self, cost: int, power: int, name: str) -> None:
        self.name: str = name
        self.cost: int = cost
        self.power: int = power
        self.atLocation: Location.Location | None = None
        self.player: Player.Player | None = None
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

    def getPower(self) -> int:
        return self.power + sum(self.otherPowerSources.values())

    def ongoing(self, game: Game.Game):
        return None

    def onReveal(self, game: Game.Game):
        event = Event.CardRevealed(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        self.revealed = True
        return None

    def onDestroy(self, game: Game.Game):
        event = Event.CardDestroyed(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        return None

    def onMove(self, game: Game.Game, toLocation: Location.Location):
        event = Event.CardMoved(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        self.atLocation = toLocation
        return None

    def onDiscard(self, game: Game.Game):
        event = Event.CardDiscarded(
            player=self.player, card=self, location=self.atLocation)
        gameHistory.addEvent(event=event)
        return None

    def summon(self, game: Game.Game):
        return None


# Abstract (but slightly more specialized) classes
#
#

class PredictCard(Card):

    def __init__(self, cost: int, power: int, name: str, predFunc: function, *args) -> None:
        super().__init__(cost, power, name)
        self.predFunc = predFunc
        self.args = args

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        if (self.atLocation.cardPlayedThisTurn[1 - self.player.playerIdx]):
            self.predFunc(*self.args)


class PredictCardPowerGain(Card):

    def __init__(self, cost: int, power: int, name: str, predPowerGain: int):
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

    def __init__(self, cost: int = 0, power: int = 2, name: str = "Yellowjacket"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        revealedCardsAtLocation = self.atLocation.getRevealedCards(
            self.player.playerIdx)
        for card in revealedCardsAtLocation:
            if card != self:
                card.power -= 1


class Mantis(PredictCard):

    def __init__(self, cost: int = 1, power: int = 2, name: str = "Mantis", *args):
        super().__init__(cost, power, name, self.drawCard, *args)

    def drawCard(self):
        self.player.drawCard()


class MistyKnight(Card):

    def __init__(self, cost: int = 1, power: int = 2, name: str = "Misty Knight"):
        super().__init__(cost, power, name)


class AntMan(Card):

    def __init__(self, cost: int = 1, power: int = 1, name: str = "Ant-Man"):
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

    def __init__(self, cost: int = 1, power: int = 1, name: str = "Elektra"):
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

    def __init__(self, cost: int = 1, power: int = 2, name: str = "Agent 13"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        FLAT_CARD_DICT = getFlatCardDict()
        randomCard = random.choice(list(FLAT_CARD_DICT.values()))()
        self.player.hand.addCard(randomCard)


class Blade(Card):

    def __init__(self, cost: int = 1, power: int = 3, name: str = "Blade"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        randomCardInHand = self.player.hand.getRandomCard()
        if randomCardInHand:
            self.player.hand.removeCard(randomCardInHand)
            randomCardInHand.onDiscard(game=game)


class Deadpool(Card):

    def __init__(self, cost: int = 1, power: int = 1, name: str = "Deadpool"):
        super().__init__(cost, power, name)

    def onDestroy(self, game: Game.Game):
        super().onDestroy(game=game)
        currentPower = self.getPower()
        self.player.hand.addCard(Deadpool(power=currentPower * 2))


class HumanTorch(Card):

    def __init__(self, cost: int = 1, power: int = 2, name: str = "Human Torch"):
        super().__init__(cost, power, name)

    def onMove(self, game: Game.Game, toLocation):
        super().onMove(game=game, toLocation=toLocation)
        self.power = self.power * 2


class Iceman(Card):

    def __init__(self, cost: int = 1, power: int = 2, name: str = "Iceman"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game):
        super().onReveal(game=game)
        target_hand = game.getPlayerByIdx(1 - self.player.playerIdx).hand
        if target_hand.getNumCards() > 0:
            target_cards = target_hand.getCards()
            target_cards[random.randint(
                0, target_hand.getNumCards() - 1)].cost += 1


class Shocker(Card):

    def __init__(self, cost: int = 2, power: int = 3, name: str = "Shocker"):
        super().__init__(cost, power, name)


class StarLord(PredictCardPowerGain):

    def __init__(self, cost: int = 2, power: int = 2, name: str = "Star Lord", predPowerGain: int = 3):
        super().__init__(cost, power, name, predPowerGain)


class Cyclops(Card):

    def __init__(self, cost: int = 3, power: int = 4, name: str = "Cyclops"):
        super().__init__(cost, power, name)


class Groot(PredictCardPowerGain):

    def __init__(self, cost: int = 3, power: int = 3, name: str = "Groot", predPowerGain: int = 3):
        super().__init__(cost, power, name, predPowerGain)


class TheThing(Card):

    def __init__(self, cost: int = 4, power: int = 6, name: str = "The Thing"):
        super().__init__(cost, power, name)


class Abomination(Card):

    def __init__(self, cost: int = 5, power: int = 9, name: str = "Abomination"):
        super().__init__(cost, power, name)


class Hulk(Card):

    def __init__(self, cost: int = 6, power: int = 12, name: str = "Hulk"):
        super().__init__(cost, power, name)


class AbsorbingMan(Card):

    def __init__(self, cost: int = 4, power: int = 4, name: str = "Absorbing Man"):
        super().__init__(cost, power, name)

    def onReveal(self, game: Game.Game = None):
        return super().onReveal(game)

    # TODO: check if last card has onReveal function
    # if yes -> this will copy it
    def lastCardPlayed(self, game: Game.Game = None):
        for t in range(game.turn, -1, -1):
            for event in game.gameHistory[t]:
                pass


class AdamWarlock(Card):

    def __init__(self, cost: int = 2, power: int = 0, name: str = "Adam Warlock"):
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
    print(len(FCD))
