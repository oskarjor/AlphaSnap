import unittest

from marvelsnap import Deck
from marvelsnap import Card


class TestDeck(unittest.TestCase):

    def test_deck(self):
        deck = Deck.Deck([Card.MistyKnight(), Card.AntMan(), Card.Wasp()])
        self.assertEqual(deck.getNumCards(), 3)
        removedCard = deck.removeCardByIndex()
        self.assertEqual(type(removedCard), Card.MistyKnight)
        self.assertEqual(deck.getNumCards(), 2)
        secondRemovedCard = deck.removeCardByIndex(1)
        self.assertEqual(type(secondRemovedCard), Card.Wasp)
        _ = deck.removeCardByIndex()
        with self.assertRaises(IndexError):
            deck.removeCardByIndex()

    def test_duplicateCards(self):
        with self.assertRaises(ValueError):
            _ = Deck.Deck([Card.MistyKnight(), Card.MistyKnight()])

    def test_nonExistentCard(self):
        with self.assertRaises(ValueError):
            deck = Deck.Deck([])
            deck.createCardsFromCardNames(["aStupidCardThatDoesNotExist"])
