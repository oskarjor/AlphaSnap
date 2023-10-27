import random

import Player
from Board import Board
import utils.GLOBAL_CONSTANTS
from Card import Card
from Location import Location
import pprint
from GameHistory import gameHistory
from utils import GLOBAL_CONSTANTS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass


class Game(object):

    def __init__(self, board: Board, player0: Player.Player, player1: Player.Player) -> None:
        self.board = board
        self.player0 = player0
        self.player1 = player1
        self.turn = 0
        self.stage = -1

        # a dict of everything that has happened during the game
        # Format
        # {
        #   turn : [event_1, event_2, event_3, event_4, ...]
        #   turn : [event_1, event_2, event_3, event_4, ...]
        #   turn : [event_1, event_2, event_3, event_4, ...]
        # }
        # event_i = [eventType, ...]
        #
        # GAME ACTIONS:
        # eventType = turnStart                 ->      turn : ["turnStarted"]       (check)
        # eventType = turnEnd                   ->      turn : ["turnEnded"]         (check)
        # eventType = gameStarted               ->      turn : ["gameStarted"]       (check)
        # eventType = gameEnded                 ->      turn : ["gameEnded", result] (check)

        self.gameHistory = gameHistory

    def getLegalMoves(self, player: Player.Player):
        legalMoves = []
        for card in player.hand.cards:
            for location in self.board.locations:
                if (player.playIsLegal(card, location)):
                    legalMoves.append([card, location])
        legalMoves.append(None)
        return legalMoves

    def getPlayerByIdx(self, idx: int):
        if idx == 0:
            return player0
        elif idx == 1:
            return player1
        return None

    def updateTurn(self, turn):
        self.turn = turn
        self.gameHistory.updateTurn(self.turn)
        self.player0.availableEnergy = self.turn
        self.player1.availableEnergy = self.turn
        event = GLOBAL_CONSTANTS.TURN_STARTED()
        self.gameHistory.addEvent(turn=self.turn, event=event)

    def triggerAllLocationAbilities(self):
        for loc in self.board.locations:
            loc.locationAbility(self)

    def startGame(self) -> None:
        event = GLOBAL_CONSTANTS.GAME_STARTED()
        self.gameHistory.addEvent(turn=self.turn, event=event)
        self.board.setupLocations()

    def beginTurn(self):
        self.updateTurn(self.turn + 1)
        self.stage = utils.GLOBAL_CONSTANTS.TURN_STAGES["BEFORE_TURN"]
        self.triggerAllLocationAbilities()
        # reset all information stored from previous turn and update turn

        for location in self.board.locations:
            # TODO: (soon deprecated) cardPlayedThisTurn should use playHistory
            location.cardPlayedThisTurn = [False, False]
            location.turn = self.turn

        self.player0.drawCard()
        self.player1.drawCard()
        player0Starts = self.board.playerIsStarting(player=self.player0)
        self.player0.isStarting = player0Starts == self.player0.playerIdx
        self.player1.isStarting = player0Starts == self.player1.playerIdx
        # print("NUMCARDS", self.player0.hand.getNumCards())

    def playTurn(self):
        self.stage = utils.GLOBAL_CONSTANTS.TURN_STAGES["DURING_TURN"]
        self.triggerAllLocationAbilities()
        player0PlayQueue = []
        player1PlayQueue = []
        while True:
            legalMoves = self.getLegalMoves(self.player0)
            moveToPlay = self.player0.selectMove(legalMoves)
            playedMove = self.player0.playMove(moveToPlay)
            if (playedMove == None):
                break
            player0PlayQueue.append(playedMove + [self.player0])

        while True:
            legalMoves = self.getLegalMoves(self.player1)
            moveToPlay = self.player1.selectMove(legalMoves)
            playedMove = self.player1.playMove(moveToPlay)
            if (playedMove == None):
                break
            player1PlayQueue.append(playedMove + [self.player1])

        playQueue = []
        if self.player0.isStarting:
            playQueue = player0PlayQueue + player1PlayQueue
        else:
            playQueue = player1PlayQueue + player0PlayQueue

        for move in playQueue:
            card, location, player = move
            event = GLOBAL_CONSTANTS.CARD_PLAYED(
                player=player, card=card, location=location)
            self.gameHistory.addEvent(turn=self.turn, event=event)

        return playQueue

    def endTurn(self):
        self.stage = utils.GLOBAL_CONSTANTS.TURN_STAGES["AFTER_TURN"]
        self.triggerAllLocationAbilities()
        for loc in self.board.locations:
            loc.triggerAllOngoing(self.player0.playerIdx, self)
            loc.triggerAllOngoing(self.player1.playerIdx, self)
        event = GLOBAL_CONSTANTS.TURN_ENDED()
        self.gameHistory.addEvent(turn=self.turn, event=event)

    def revealCards(self, playQueue: list[Card, Location, Player.Player]):
        for card, location, player in playQueue:
            print(f"Player {player} played {card} at {location}!")
            card.onReveal(self)
            card.ongoing(self)

    def endGame(self):
        gameWinner = self.board.playerIsWinning(player0)
        if (gameWinner == 1):
            event = GLOBAL_CONSTANTS.GAME_ENDED(result=player0)
            print("Player 0 wins!")
        elif (gameWinner == -1):
            event = GLOBAL_CONSTANTS.GAME_ENDED(result=player1)
            print("Player 1 wins!")
        elif (gameWinner == 0):
            event = GLOBAL_CONSTANTS.GAME_ENDED(result=None)
            print("It's a tie!")
        self.gameHistory.addEvent(turn=self.turn, event=event)

    def playGame(self):
        game.startGame()
        print("Player 0 deck: ", str(self.player0.deck))
        print("Player 1 deck: ", str(self.player1.deck))
        for i in range(1, 7):
            print("-" * 124)
            print(f"ROUND {i}")
            print("-" * 124)
            self.beginTurn()
            movesPlayed = self.playTurn()
            self.revealCards(movesPlayed)
            self.endTurn()
            print("-" * 124)
            print()
            self.visualizeBoard(self.board)
            if (i == 6):
                self.endGame()
                continue
            play_next_turn = input("Do you wish to play next turn [y/n]: ")
            if play_next_turn.lower() == "y":
                print("\n")
                continue
            elif play_next_turn.lower() == "n":
                print("Game aborted")
                break
        # pprint.pprint(self.gameHistory)

    def visualizeBoard(self, board: Board):
        player0Cards = []
        player1Cards = []
        allLocations = []
        for i, location in enumerate(board.locations):
            player0Cards.append(location.getCards(0).copy())
            player1Cards.append(location.getCards(1).copy())
            player0Cards[i] += [''] * (4 - len(player0Cards[i]))
            player1Cards[i] += [''] * (4 - len(player1Cards[i]))
            allLocations.append(location)

        print("Player 1 (opponent):")
        print("Hand:", player1.hand)
        print("-" * 124)
        for i in range(3, -1, -1):
            print(f"| Spot {i+1} | {str(player1Cards[0][i]).center(35)} | {
                  str(player1Cards[1][i]).center(35)} | {str(player1Cards[2][i]).center(35)} |")
        print("-" * 124)
        print(f"| | {str(allLocations[0].getTotalPower(1)).center(35)} | {str(
            allLocations[1].getTotalPower(1)).center(35)} | {str(allLocations[2].getTotalPower(1)).center(35)} |")
        print(f"| | {str(allLocations[0]).center(35)} | {
              str(allLocations[1]).center(35)} | {str(allLocations[2]).center(35)} |")
        print(f"| | {str(allLocations[0].getTotalPower(0)).center(35)} | {str(
            allLocations[1].getTotalPower(0)).center(35)} | {str(allLocations[2].getTotalPower(0)).center(35)} |")
        print("-" * 124)
        for i in range(0, 4, 1):
            print(f"| Spot {i+1} | {str(player0Cards[0][i]).center(35)} | {
                  str(player0Cards[1][i]).center(35)} | {str(player0Cards[2][i]).center(35)} |")
        print("-" * 124)
        print("Player 0 (you):")
        print("Hand:", player0.hand)
        print("")


if __name__ == "__main__":
    import Card
    FLAT_CARD_DICT = Card.getFlatCardDict()
    board = Board()
    cardNames0 = random.sample(list(FLAT_CARD_DICT.keys()), 6)
    cardNames1 = random.sample(list(FLAT_CARD_DICT.keys()), 6)
    player0 = Player.Player(cardNames=cardNames0, playerIdx=0)
    player1 = Player.Player(cardNames=cardNames1, playerIdx=1)
    game = Game(board, player0, player1)
    game.playGame()
