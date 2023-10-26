import unittest
import random

import Player
import Board
import Location


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board.Board()
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_Board(self) -> None:
        for loc in self.board.locations:
            self.assertEqual(loc, None)
        self.assertEqual(len(self.board.locations), 3)

        LOCATION_DICT = Location.getFlatLocationDict()
        locations = random.sample(list(LOCATION_DICT.keys()), 3)

        self.board.setupLocations(locations)

        for loc in self.board.locations:
            self.assertNotEqual(loc, None)
            self.assertIn(Location.Location, type(loc).mro())
        self.assertEqual(len(self.board.locations), 3)
