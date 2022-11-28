from __future__ import annotations

from typing import TYPE_CHECKING

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

    def __str__(self) -> str:
        return f"{self.name} ({self.idx})"

    def locationAbility(self, game: Game.Game = None):
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
        return sum([card.getPower() for card in self.getRevealedCards(playerIdx)]) + sum(self.otherPowerSources.values())

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

    def playerIsWinning(self, player: Player.Player):
        selfPower = self.getTotalPower(playerIdx=player.playerIdx)
        opposingPower = self.getTotalPower(playerIdx=(1 - player.playerIdx))
        if(selfPower > opposingPower):
            return 1
        if(selfPower == opposingPower):
            return 0
        if(selfPower < opposingPower):
            return -1


class Ruins(Location):

    def __init__(self, idx, name= "Ruins", cardSpaces=[4, 4], desc="A ruined land") -> None:
        super().__init__(name, idx, cardSpaces, desc)

class Asgard(Location):

    def __init__(self, idx: int, name="Asgard", cardSpaces=[4, 4], desc="After turn 4, whoever is winning here draws 2 cards.") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self, game: Game.Game):
        super().locationAbility(game)
        if(game.turn == 4 and game.stage == utils.GLOBAL_CONSTANTS.TURN_STAGES["AFTER_TURN"]):
            if(self.playerIsWinning(game.player0) == 1):
                print("Asgard: player0 drew 2 cards!")
                game.player0.drawCard()
                game.player0.drawCard()
            if(self.playerIsWinning(game.player1) == 1):
                print("Asgard: player1 drew 2 cards!")
                game.player1.drawCard()
                game.player1.drawCard()

class Atlantis(Location):

    def __init__(self, idx, name="Atlantis", cardSpaces=[4, 4], desc="If you only have one card here, it has +5 Power") -> None:
        super().__init__(idx, name, cardSpaces, desc)

    def locationAbility(self, game: Game.Game = None):
        super().locationAbility(game)
        for i in [game.player0.playerIdx, game.player1.playerIdx]:
            if(len(self.cards[i]) == 1):
                if(self in self.cards[i][0].otherPowerSources.keys()):
                    continue
                print(f"Atlantis: {self.cards[i][0]} gained power")
                self.cards[i][0].otherPowerSources[self] = 5
            else:
                for card in self.cards[i]:
                    cardPopped = card.otherPowerSources.pop(self, None)
                    if(cardPopped != None):
                        print(f"Atlantis: {self.cards[i][0]} lost bonus power")
