import unittest

import Card
import Location
import Player
import Deck
import Hand
import Game


class TestCards(unittest.TestCase):

    def setUp(self) -> None:
        self.location = Location.Ruins(0)
        self.player0 = Player.Player([], playerIdx=0, availableEnergy=0)
        self.player1 = Player.Player([], playerIdx=1, availableEnergy=0)

    def test_card(self):
        mistyKnight = Card.MistyKnight()
        self.assertEqual(mistyKnight.cost, 1)
        self.assertEqual(mistyKnight.power, 2)
        self.assertEqual(mistyKnight.name, "Misty Knight")
        self.assertEqual(mistyKnight.atLocation, None)
        self.assertEqual(mistyKnight.player, None)
        self.assertEqual(mistyKnight.revealed, False)
        self.assertEqual(str(mistyKnight), "Misty Knight (C: 1, P: 2)")

    def test_tooManyCards(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        mistyKnight3 = Card.MistyKnight()
        mistyKnight4 = Card.MistyKnight()
        mistyKnight5 = Card.MistyKnight()

        self.location.addCard(mistyKnight1, self.player0)
        self.location.addCard(mistyKnight2, self.player0)
        self.location.addCard(mistyKnight3, self.player0)
        self.location.addCard(mistyKnight4, self.player0)
        with self.assertRaises(ValueError):
            self.location.addCard(mistyKnight5, self.player0)

    def test_plainCards(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        shocker = Card.Shocker()
        cyclops = Card.Cyclops()

        self.location.addCard(mistyKnight1, self.player0)
        self.location.addCard(mistyKnight2, self.player0)
        self.location.triggerOnReveal(mistyKnight1, None)
        self.location.triggerOnReveal(mistyKnight2, None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2)

        self.location.addCard(shocker, self.player1)
        self.location.addCard(cyclops, self.player1)
        self.location.triggerOnReveal(shocker, None)
        self.location.triggerOnReveal(cyclops, None)
        self.assertEqual(self.location.getTotalPower(
            self.player1.playerIdx), 3+4)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2)

    def test_antMan(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        mistyKnight3 = Card.MistyKnight()
        antMan = Card.AntMan()

        self.location.addCard(mistyKnight1, self.player0)
        self.location.addCard(mistyKnight2, self.player0)
        self.location.addCard(antMan, self.player0)
        self.location.triggerOnReveal(mistyKnight1, None)
        self.location.triggerOnReveal(mistyKnight2, None)
        self.location.triggerOnReveal(antMan, None)

        antMan.ongoing(None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

        self.location.addCard(mistyKnight3, self.player0)
        antMan.ongoing(None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2+4)
        self.assertTrue(antMan.ongoingTriggered)

        self.location.triggerOnReveal(mistyKnight3, None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2+2+4)

        self.location.removeCard(mistyKnight1, self.player0.playerIdx)
        antMan.ongoing(None)
        self.assertEqual(self.location.getAmountOfCards(
            self.player0.playerIdx), 3)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

    def test_starLordNotTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(starLord, self.player0)
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(starLord, None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2)

    def test_starLordTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(starLord, self.player1)
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(starLord, None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2)
        self.assertEqual(self.location.getTotalPower(
            self.player1.playerIdx), 5)

    def test_elektra(self):
        mistyKnight = Card.MistyKnight()
        theThing = Card.TheThing()
        elektra = Card.Elektra()

        # when cards are not revealed, no cards are removed
        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(theThing, self.player0)
        self.location.addCard(elektra, self.player1)
        self.assertEqual(self.location.triggerOnReveal(elektra, None), None)
        self.assertEqual(self.location.getAmountOfCards(
            self.player0.playerIdx), 2)

        # reveal the two opposing cards, make sure misty knight is removed
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(theThing, None)
        removedCard = self.location.triggerOnReveal(elektra, None)
        self.assertEqual(removedCard, mistyKnight)
        self.assertEqual(self.location.getAmountOfCards(
            self.player0.playerIdx), 1)

    def test_yellowjacket(self):
        revealedMistyKnight = Card.MistyKnight()
        unrevealedMistyKnight = Card.MistyKnight()
        opposingMistyKnight = Card.MistyKnight()
        yellowjacket = Card.Yellowjacket()

        self.location.addCard(revealedMistyKnight, self.player0)
        self.location.triggerOnReveal(revealedMistyKnight, None)
        self.location.addCard(unrevealedMistyKnight, self.player0)
        self.location.addCard(opposingMistyKnight, self.player1)
        self.location.addCard(yellowjacket, self.player0)
        self.location.triggerOnReveal(opposingMistyKnight, None)
        self.location.triggerOnReveal(yellowjacket, None)
        self.location.triggerOnReveal(unrevealedMistyKnight, None)
        self.assertEqual(self.location.getTotalPower(
            self.player0.playerIdx), 2+2+1)
        self.assertEqual(self.location.getTotalPower(
            self.player1.playerIdx), 2)

        self.assertEqual(revealedMistyKnight.power, 1)
        self.assertEqual(unrevealedMistyKnight.power, 2)
        self.assertEqual(yellowjacket.power, 2)

    def test_mantisTrigger(self):
        mistyKnight = Card.MistyKnight()
        mantis = Card.Mantis()
        self.player1.deck = Deck.Deck(["Misty Knight", "Ant-Man"])

        prevHandSize = self.player1.hand.getNumCards()
        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(mantis, self.player1)
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(mantis, None)
        self.assertEqual(self.player1.hand.getNumCards(), prevHandSize + 1)

    def test_mantisNotTrigger(self):
        mantis = Card.Mantis()
        self.player1.deck = Deck.Deck(["Misty Knight", "Ant-Man"])

        prevHandSize = self.player1.hand.getNumCards()
        self.location.addCard(mantis, self.player1)
        self.location.triggerOnReveal(mantis, None)
        self.assertEqual(self.player1.hand.getNumCards(), prevHandSize)

    def test_agent13(self):
        agent13 = Card.Agent13()
        self.player0.hand = Hand.Hand()
        self.assertEqual(self.player0.hand.getNumCards(), 0)

        self.location.addCard(agent13, player=self.player0)
        self.location.triggerOnReveal(agent13, None)
        self.assertEqual(self.location.getTotalPower(0), 2)

        self.assertEqual(self.player0.hand.getNumCards(), 1)
        self.assertIn(Card.Card, type(self.player0.hand.getCards()[0]).mro())

    def test_deadpool(self):

        deadpool1 = Card.Deadpool()
        self.player0.hand = Hand.Hand()
        self.assertEqual(self.player0.hand.getNumCards(), 0)

        self.location.addCard(deadpool1, player=self.player0)
        self.location.triggerOnReveal(deadpool1, None)
        self.assertEqual(self.location.getTotalPower(0), 1)
        self.assertEqual(self.player0.hand.getNumCards(), 0)

        self.location.destroyCard(deadpool1, player=self.player0, game=None)

        self.assertEqual(self.location.getTotalPower(0), 0)
        self.assertEqual(self.player0.hand.getNumCards(), 1)

        self.assertEqual(type(self.player0.hand.getCards()[0]), Card.Deadpool)

        deadpool2 = self.player0.hand.getCards()[0]
        self.location.addCard(deadpool2, player=self.player0)
        self.location.triggerOnReveal(deadpool2, None)

        self.assertEqual(self.location.getTotalPower(0), 2)

    def test_adamWarlockTrigger(self):
        mistyKnight = Card.MistyKnight()
        abomination = Card.Abomination()
        adamWarlock = Card.AdamWarlock()
        self.player0.deck = Deck.Deck(["Misty Knight", "Ant-Man"])

        prevHandSize = self.player0.hand.getNumCards()
        self.location.addCard(mistyKnight, self.player1)
        self.location.addCard(adamWarlock, self.player0)
        self.location.addCard(abomination, self.player0)
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(adamWarlock, None)
        self.location.triggerOnReveal(abomination, None)

        self.location.triggerAllOngoing(
            playerIdx=self.player0.playerIdx, game=None)
        newHandSize = self.player0.hand.getNumCards()
        self.assertEqual(prevHandSize + 1, newHandSize)

    def test_adamWarlockNotTrigger(self):
        mistyKnight = Card.MistyKnight()
        adamWarlock = Card.AdamWarlock()
        self.player0.deck = Deck.Deck(["Misty Knight", "Ant-Man"])

        prevHandSize = self.player0.hand.getNumCards()
        self.location.addCard(mistyKnight, self.player1)
        self.location.addCard(adamWarlock, self.player0)
        self.location.triggerOnReveal(mistyKnight, None)
        self.location.triggerOnReveal(adamWarlock, None)

        self.location.triggerAllOngoing(
            playerIdx=self.player0.playerIdx, game=None)
        newHandSize = self.player0.hand.getNumCards()
        self.assertEqual(prevHandSize, newHandSize)


if __name__ == "__main__":
    unittest.main()
