import unittest

import Card
import Location
import Player

class TestLocations(unittest.TestCase):

    def setUp(self) -> None:
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_ruinsLocation(self):
        location = Location.Ruins(0)

        # the location starts with 0 cards
        self.assertEqual(location.getAmountOfCards(0), 0)
        self.assertEqual(location.getAmountOfCards(1), 0)

        # the location can store up to four cards
        self.assertEqual(location.cardSpaces[0], 4)
        self.assertEqual(location.cardSpaces[1], 4)

    def test_atlantisLocation(self):
        atlantisLocation = Location.Atlantis(0)

        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        opposingMistyKnight1 = Card.MistyKnight()
        opposingMistyKnight2 = Card.MistyKnight()

        atlantisLocation.addCard(mistyKnight1, self.player0)
        atlantisLocation.addCard(mistyKnight2, self.player0)
        atlantisLocation.addCard(opposingMistyKnight1, self.player1)
        atlantisLocation.triggerOnReveal(mistyKnight1)
        atlantisLocation.triggerOnReveal(mistyKnight2)
        atlantisLocation.triggerOnReveal(opposingMistyKnight1)

        self.assertEqual(atlantisLocation.getTotalPower(self.player0.playerIdx), 2+2)
        self.assertEqual(atlantisLocation.getTotalPower(self.player1.playerIdx), 2)

        atlantisLocation.locationAbility()

        self.assertEqual(atlantisLocation.getTotalPower(self.player0.playerIdx), 2+2)
        self.assertEqual(atlantisLocation.getTotalPower(self.player1.playerIdx), 2+5)

        atlantisLocation.removeCard(mistyKnight1, self.player0.playerIdx)
        atlantisLocation.addCard(opposingMistyKnight2, self.player1)
        atlantisLocation.triggerOnReveal(opposingMistyKnight2)
        atlantisLocation.locationAbility()

        self.assertEqual(atlantisLocation.getTotalPower(self.player0.playerIdx), 2+5)
        self.assertEqual(atlantisLocation.getTotalPower(self.player1.playerIdx), 2+2)

        