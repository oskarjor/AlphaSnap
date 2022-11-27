import unittest

import Deck
import Card

class TestDeck(unittest.TestCase):

    def test_deck(self):
        deck = Deck.Deck(["mistyKnight", "antMan", "wasp"])
        self.assertEqual(deck.getNumCards(), 3)
        removedCard = deck.removeCard()
        self.assertEqual(type(removedCard), Card.MistyKnight)
        self.assertEqual(deck.getNumCards(), 2)
        secondRemovedCard = deck.removeCard(1)
        self.assertEqual(type(secondRemovedCard), Card.Wasp)
        _ = deck.removeCard()
        with self.assertRaises(IndexError):
            deck.removeCard()

    def test_duplicateCards(self):
        with self.assertRaises(ValueError):
            _ = Deck.Deck(["mistyKnight", "mistyKnight"])

    def test_nonExistentCard(self):
        with self.assertRaises(ValueError):
            _ = Deck.Deck(["aSupidCardThatDoesNotExist"])


