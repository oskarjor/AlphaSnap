from marvelsnap import Board, Player, Game
from marvelsnap.GameHistory import gameHistory
import random

if __name__ == "__main__":
    import Card
    FLAT_CARD_DICT = Card.getFlatCardDict()
    board = Board()
    cards0 = [card() for card in random.sample(
        list(FLAT_CARD_DICT.values()), 6)]
    cards1 = [card() for card in random.sample(
        list(FLAT_CARD_DICT.values()), 6)]
    player0 = Player.Player(cards=cards0, playerIdx=0)
    player1 = Player.Player(cards=cards1, playerIdx=1)
    game = Game(board, player0, player1)
    game.playGame()
    print(gameHistory)
