import unittest

import Player
import Card
import Location


class TestDeck(unittest.TestCase):

    def test_init(self):
        player = Player.Player([], playerIdx=0)
        self.assertEqual(player.playerIdx, 0)
        self.assertEqual(player.availableEnergy, 0)
        self.assertEqual(str(player), "0")
        self.assertEqual(len(player.deck), 0)

    def test_wrongInit(self):
        with self.assertRaises(TypeError):
            _ = Player.Player([])

    def test_deckInit(self):
        player = Player.Player(
            [Card.MistyKnight(), Card.AntMan(), Card.Mantis()], playerIdx=0)
        self.assertEqual(len(player.deck), 3)

    def test_drawCard(self):
        player = Player.Player(
            [Card.MistyKnight(), Card.AntMan(), Card.Mantis()], playerIdx=0)
        self.assertEqual(len(player.deck), 3)
        self.assertEqual(len(player.hand), 0)
        player.drawCard()
        self.assertEqual(len(player.deck), 2)
        self.assertEqual(len(player.hand), 1)
        player.drawCard()
        self.assertEqual(len(player.deck), 1)
        self.assertEqual(len(player.hand), 2)
        player.drawCard()
        self.assertEqual(len(player.deck), 0)
        self.assertEqual(len(player.hand), 3)
        self.assertTrue(player.deck.isEmpty())
        self.assertFalse(player.drawCard())

    def test_playMove(self):
        mk = Card.MistyKnight()
        am = Card.AntMan()
        ma = Card.Mantis()
        player = Player.Player(
            [mk, am, ma], playerIdx=0, availableEnergy=1000)
        loc = Location.Ruins(idx=0)
        with self.assertRaises(KeyError):
            player.playMove([mk, loc])
        player.drawCard()
        self.assertEqual(player.hand.getCards()[0], mk)
        player.playMove([mk, loc])
        self.assertEqual(player.hand.getNumCards(), 0)

    def test_tooLittleEnergy(self):
        mk = Card.MistyKnight()
        player = Player.Player([], playerIdx=0, availableEnergy=0)
        player.hand.addCard(mk)
        loc = Location.Ruins(0)
        self.assertFalse(player.playIsLegal(player.hand.getCards()[0], loc))

        player.availableEnergy = 100
        self.assertTrue(player.playIsLegal(player.hand.getCards()[0], loc))
