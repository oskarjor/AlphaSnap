import unittest

import Card
import Location
import Player

class TestLocations(unittest.TestCase):

    def setUp(self) -> None:
        self.location = Location.RuinsLocation(0)
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_Location(self):
        pass

    def test_RuinsLocation(self):
        pass