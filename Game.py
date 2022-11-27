import random

from Player import Player
from Board import Board
from Card import Card
from Location import Location

class Game(object):
    
    def __init__(self, board: Board, player1: Player, player2: Player) -> None:
        self.board = board
        self.player0 = player1
        self.player1 = player2
        self.turn = 0
    
    def startGame(self) -> None:
        self.board.setupLocations()

    def beginTurn(self):
        # reset all information stored from previous turn
        for location in self.board.locations:
            location.cardPlayedThisTurn = [False, False]
        
        self.turn += 1
        self.player0.drawCard()
        self.player1.drawCard()
        # TODO: should not be random, but rather based on who is currently winning
        player0Starts = self.board.playerIsStarting(player=self.player0)
        self.player0.availableEnergy = self.turn
        self.player1.availableEnergy = self.turn
        self.player0.isStarting = player0Starts == self.player0.playerIdx
        self.player1.isStarting = player0Starts == self.player1.playerIdx

    def getLegalMoves(self, player: Player):
        legalMoves = []
        for card in player.hand:
            for location in self.board.locations:
                if(player.playIsLegal(card, location)):
                    legalMoves.append([card, location])
        legalMoves.append(None)
        return legalMoves

    def playTurn(self):
        self.beginTurn()
        player0PlayQueue = []
        player1PlayQueue = []
        while True:
            legalMoves = self.getLegalMoves(self.player0)
            playedMove = self.player0.playMove(legalMoves)
            if(playedMove == None):
                break
            player0PlayQueue.append(playedMove + [self.player0])
        
        while True:
            legalMoves = self.getLegalMoves(self.player1)
            playedMove = self.player1.playMove(legalMoves)
            if(playedMove == None):
                break
            player1PlayQueue.append(playedMove + [self.player1])

        playQueue = []
        if self.player0.isStarting:
            playQueue = player0PlayQueue + player1PlayQueue
        else:
            playQueue = player1PlayQueue + player0PlayQueue

        return playQueue

    def endGame(self):
        gameWinner = self.board.playerIsWinning(player0)
        if(gameWinner == 1):
            print("Player 0 wins!")
        elif(gameWinner == -1):
            print("Player 1 wins!")
        elif(gameWinner == 0):
            print("It's a tie!")

    def revealCards(self, playQueue: list[Card, Location, Player]):
        for card, location, player in playQueue:
            print(f"Player {player} played {card} at {location}!")
            card.onReveal()
            card.ongoing()

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
        print("-" * 124)
        for i in range(3, -1, -1):
            print(f"| Spot {i+1} | {str(player1Cards[0][i]).center(35)} | {str(player1Cards[1][i]).center(35)} | {str(player1Cards[2][i]).center(35)} |")
        print("-" * 124)
        print(f"|        | {str(allLocations[0].getTotalPower(1)).center(35)} | {str(allLocations[1].getTotalPower(1)).center(35)} | {str(allLocations[2].getTotalPower(1)).center(35)} |")
        print(f"|        | {str(allLocations[0]).center(35)} | {str(allLocations[1]).center(35)} | {str(allLocations[2]).center(35)} |")
        print(f"|        | {str(allLocations[0].getTotalPower(0)).center(35)} | {str(allLocations[1].getTotalPower(0)).center(35)} | {str(allLocations[2].getTotalPower(0)).center(35)} |")
        print("-" * 124)
        for i in range(0, 4, 1):
            print(f"| Spot {i+1} | {str(player0Cards[0][i]).center(35)} | {str(player0Cards[1][i]).center(35)} | {str(player0Cards[2][i]).center(35)} |")
        print("-" * 124)
        print("Player 0 (you):")
        print("")


if __name__ == "__main__":
    board = Board()
    cardNames0 = ["mistyKnight", "cyclops"]
    cardNames1 = ["shocker", "abomination"]
    player0 = Player(cardNames=cardNames0, playerIdx=0)
    player1 = Player(cardNames=cardNames1, playerIdx=1)
    game = Game(board, player0, player1)
    game.startGame()
    for i in range(1, 7):
        print("-" * 124)
        print(f"ROUND {i}")
        print("-" * 124)
        movesPlayed = game.playTurn()
        game.revealCards(movesPlayed)
        print("-" * 124)
        print()
        game.visualizeBoard(game.board)
        if(i == 6):
            game.endGame()
            continue
        play_next_turn = input("Do you wish to play next turn [y/n]: ")
        if play_next_turn.lower() == "y":
            print("\n")
            continue
        elif play_next_turn.lower() == "n":
            print("Game aborted")
            break

