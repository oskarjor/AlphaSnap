import unittest

import Card
import Location
import Player

class TestLocations(unittest.TestCase):

    def setUp(self) -> None:
        self.location = Location.RuinsLocation(0)
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_RuinsLocation(self):
        # the location starts with 0 cards
        self.assertEqual(self.location.getAmountOfCards(0), 0)
        self.assertEqual(self.location.getAmountOfCards(1), 0)

        # the location can store up to four cards
        self.assertEqual(self.location.cardSpaces[0], 4)
        self.assertEqual(self.location.cardSpaces[1], 4)