from __future__ import annotations

from typing import TYPE_CHECKING
from utils.utils import all_subclasses

from Card import Card

if TYPE_CHECKING:
    import Game
    import Player

import utils.GLOBAL_CONSTANTS


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
        self.otherPowerSources = {}
        # cards can be played here. Note that if this is false, but notLocked is True, cards can
        self.canPlayHere = True
        # still be moved from and to this location.
        # location is locked. No cards can be moved from here or to here, played here
        self.locked = False
        # or summoned here (Professor X effect)

    def __str__(self) -> str:
        return f"{self.name} ({self.idx})"

    def locationAbility(self, game: Game.Game = None):
        return None

    def addCard(self, card: Card, player):
        playerIdx = player.playerIdx
        if (not self.getPlayable(playerIdx=playerIdx)):
            raise ValueError("Can't add more cards here")
        self.cards[playerIdx].append(card)
        card.atLocation = self
        card.player = player
        self.cardPlayedThisTurn[playerIdx] = True

    def triggerAllOngoing(self, playerIdx: int, game: Game.Game):
        if (self.ongoinEnabled):
            for card in self.cards[playerIdx]:
                card.ongoing(game)

    def triggerOnReveal(self, card: Card, game: Game.Game):
        if (self.onRevealEnabled):
            return card.onReveal(game)

    def destroyCard(self, card: Card, player: Player.Player, game: Game.Game):
        card.onDestroy(game)
        self.removeCard(card, playerIdx=player.playerIdx)

    def removeCard(self, card: Card, playerIdx: int):
        self.cards[playerIdx].remove(card)
        # self.triggerAllOngoing(playerIdx, game)

    def getTotalPower(self, playerIdx: int):
        return sum([card.getPower() for card in self.getRevealedCards(playerIdx)]) + sum(self.otherPowerSources.values())

    def getCards(self, playerIdx: int):
        return self.cards[playerIdx]

    def getRevealedCards(self, playerIdx: int):
        return [card for card in self.cards[playerIdx] if card.revealed]

    def getAmountOfCards(self, playerIdx: int):
        return len(self.cards[playerIdx])

    def getPlayable(self, playerIdx: int):
        if (self.canPlayHere and not self.locked):
            if self.getAmountOfCards(playerIdx) < self.cardSpaces[playerIdx]:
                return True
        return False

    def playerIsWinning(self, player: Player.Player):
        selfPower = self.getTotalPower(playerIdx=player.playerIdx)
        opposingPower = self.getTotalPower(playerIdx=(1 - player.playerIdx))
        if (selfPower > opposingPower):
            return 1
        if (selfPower == opposingPower):
            return 0
        if (selfPower < opposingPower):
            return -1


class Ruins(Location):

    def __init__(self, idx, name="Ruins", cardSpaces=[4, 4], desc="A ruined land") -> None:
        super().__init__(idx, name, cardSpaces, desc)


class Asgard(Location):

    def __init__(self, idx: int, name="Asgard", cardSpaces=[4, 4], desc="After turn 4, whoever is winning here draws 2 cards.") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self, game: Game.Game):
        super().locationAbility(game)
        if (game.turn == 4 and game.stage == utils.GLOBAL_CONSTANTS.TURN_STAGES["AFTER_TURN"]):
            if (self.playerIsWinning(game.player0) == 1):
                if (utils.GLOBAL_CONSTANTS.VERBOSE > 0):
                    print("Asgard: player0 drew 2 cards!")
                game.player0.drawCard()
                game.player0.drawCard()
            if (self.playerIsWinning(game.player1) == 1):
                if (utils.GLOBAL_CONSTANTS.VERBOSE > 0):
                    print("Asgard: player1 drew 2 cards!")
                game.player1.drawCard()
                game.player1.drawCard()


class Atlantis(Location):

    def __init__(self, idx: int, name="Atlantis", cardSpaces=[4, 4], desc="If you only have one card here, it has +5 Power") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self, game: Game.Game = None):
        super().locationAbility(game)
        for i in [0, 1]:
            if (len(self.cards[i]) == 1):
                if (self in self.cards[i][0].otherPowerSources.keys()):
                    continue
                if (utils.GLOBAL_CONSTANTS.VERBOSE > 0):
                    print(f"Atlantis: {self.cards[i][0]} gained power")
                self.cards[i][0].otherPowerSources[self] = 5
            else:
                for card in self.cards[i]:
                    cardPopped = card.otherPowerSources.pop(self, None)
                    if (cardPopped != None):
                        if (utils.GLOBAL_CONSTANTS.VERBOSE > 0):
                            print(f"Atlantis: {
                                  self.cards[i][0]} lost bonus power")


class Attilan(Location):

    def __init__(self, idx: int, name="Attilan", cardSpaces=[4, 4], desc="After turn 3, shuffle your hand into your deck. Draw 3 cards.") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self, game: Game.Game = None):
        super().locationAbility(game)
        if (game.turn == 3 and game.stage == utils.GLOBAL_CONSTANTS.TURN_STAGES["AFTER_TURN"]):
            for player in [game.player0, game.player1]:
                for card in player.hand.cards:
                    player.hand.removeCard(card)
                    player.deck.addCard(card)
                player.deck.shuffle()
                for _ in range(3):
                    player.drawCard()


def getFlatLocationDict():
    FLAT_LOCATION_DICT = {}
    sub = all_subclasses(Location)
    for s in sub:
        try:
            FLAT_LOCATION_DICT[s(idx=-1).name] = s
        except:
            pass
    return FLAT_LOCATION_DICT


if __name__ == "__main__":
    print(getFlatLocationDict().keys())
