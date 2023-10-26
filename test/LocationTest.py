import unittest

import Card
import Location
import Player
import Game
import Board

import utils.GLOBAL_CONSTANTS as GLOBAL_CONSTANTS


class TestLocations(unittest.TestCase):

    def setUp(self) -> None:
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_ruins(self):
        location = Location.Ruins(0)

        # the location starts with 0 cards
        self.assertEqual(location.getAmountOfCards(0), 0)
        self.assertEqual(location.getAmountOfCards(1), 0)

        # the location can store up to four cards
        self.assertEqual(location.cardSpaces[0], 4)
        self.assertEqual(location.cardSpaces[1], 4)

    def test_atlantis(self):
        atlantisLocation = Location.Atlantis(0)

        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        opposingMistyKnight1 = Card.MistyKnight()
        opposingMistyKnight2 = Card.MistyKnight()

        atlantisLocation.addCard(mistyKnight1, self.player0)
        atlantisLocation.addCard(mistyKnight2, self.player0)
        atlantisLocation.addCard(opposingMistyKnight1, self.player1)
        atlantisLocation.triggerOnReveal(mistyKnight1, None)
        atlantisLocation.triggerOnReveal(mistyKnight2, None)
        atlantisLocation.triggerOnReveal(opposingMistyKnight1, None)

        self.assertEqual(atlantisLocation.getTotalPower(
            self.player0.playerIdx), 2+2)
        self.assertEqual(atlantisLocation.getTotalPower(
            self.player1.playerIdx), 2)

        atlantisLocation.locationAbility()

        self.assertEqual(atlantisLocation.getTotalPower(
            self.player0.playerIdx), 2+2)
        self.assertEqual(atlantisLocation.getTotalPower(
            self.player1.playerIdx), 2+5)

        atlantisLocation.removeCard(mistyKnight1, self.player0.playerIdx)
        atlantisLocation.addCard(opposingMistyKnight2, self.player1)
        atlantisLocation.triggerOnReveal(opposingMistyKnight2, None)
        atlantisLocation.locationAbility()

        self.assertEqual(atlantisLocation.getTotalPower(
            self.player0.playerIdx), 2+5)
        self.assertEqual(atlantisLocation.getTotalPower(
            self.player1.playerIdx), 2+2)

    def test_asgard(self):
        initalDeckCards = GLOBAL_CONSTANTS.SAMPLE_DECK
        initalDeckSize = len(initalDeckCards)
        board = Board.Board()
        player0 = Player.Player(initalDeckCards, 0)
        player1 = Player.Player(initalDeckCards, 0)
        game = Game.Game(board, player0, player1)
        game.updateTurn(4)

        for i in range(3):
            self.assertEqual(game.board.locations[i], None)

        game.board.setupLocations(["Ruins", "Ruins", "Asgard"])
