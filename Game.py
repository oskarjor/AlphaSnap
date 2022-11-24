import random

from Player import Player
from Board import Board
from Card import Card
from Location import Location

class Game(object):
    
    def __init__(self, board: Board, player1: Player, player2: Player) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.player1Starts = random.randint(0, 1)
        self.turn = 0
    
    def startGame(self) -> None:
        self.board.setupLocations()

    def beginTurn(self):
        # reset all information stored from previous turn
        for location in self.board.locations:
            location.cardPlayedThisTurn = [False, False]
        
        self.turn += 1
        self.player1Starts = random.randint(0, 1)
        self.player1.availableEnergy = self.turn
        self.player2.availableEnergy = self.turn
        self.player1.isStarting = self.player1Starts == self.player1.playerIdx
        self.player2.isStarting = self.player1Starts == self.player2.playerIdx

    def getLegalMoves(self, player: Player):
        legalMoves = []
        for card in player.deck.cards:
            for location in self.board.locations:
                if(player.playIsLegal(card, location)):
                    legalMoves.append([card, location])
        legalMoves.append(None)
        return legalMoves

    def playTurn(self):
        self.beginTurn()
        player1PlayQueue = []
        player2PlayQueue = []
        while True:
            legalMoves = self.getLegalMoves(self.player1)
            playedMove = self.player1.playMove(legalMoves)
            if(playedMove == None):
                break
            player1PlayQueue.append(playedMove + [self.player1])
        
        while True:
            legalMoves = self.getLegalMoves(self.player2)
            playedMove = self.player2.playMove(legalMoves)
            if(playedMove == None):
                break
            player2PlayQueue.append(playedMove + [self.player2])

        playQueue = []
        if self.player1Starts:
            playQueue = player1PlayQueue + player2PlayQueue
        else:
            playQueue = player2PlayQueue + player1PlayQueue

        return playQueue

    def revealCards(self, playQueue: list[Card, Location, Player]):
        for card, location, player in playQueue:
            print(f"Player {player} played {card} at {location}!")
            card.onReveal()
            card.ongoing()

if __name__ == "__main__":
    board = Board()
    cardNames1 = ["mistyKnight", "cyclops"]
    cardNames2 = ["shocker", "abomination"]
    player1 = Player(cardNames=cardNames1, playerIdx=0)
    player2 = Player(cardNames=cardNames2, playerIdx=1)
    game = Game(board, player1, player2)
    game.startGame()
    for i in range(1, 3):
        print(f"Round {i}")
        print("------------------------")
        movesPlayed = game.playTurn()
        for move in movesPlayed:
            card, location, player = move
            
        print("\n")

