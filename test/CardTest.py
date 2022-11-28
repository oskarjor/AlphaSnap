import unittest

import Card
import Location
import Player
import Deck

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
        self.location.triggerOnReveal(mistyKnight1)
        self.location.triggerOnReveal(mistyKnight2)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2)

        self.location.addCard(shocker, self.player1)
        self.location.addCard(cyclops, self.player1)
        self.location.triggerOnReveal(shocker)
        self.location.triggerOnReveal(cyclops)
        self.assertEqual(self.location.getTotalPower(self.player1.playerIdx), 3+4)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2)
        
    
    def test_antMan(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        mistyKnight3 = Card.MistyKnight()
        antMan = Card.AntMan()

        self.location.addCard(mistyKnight1, self.player0)
        self.location.addCard(mistyKnight2, self.player0)
        self.location.addCard(antMan, self.player0)
        self.location.triggerOnReveal(mistyKnight1)
        self.location.triggerOnReveal(mistyKnight2)
        self.location.triggerOnReveal(antMan)
        
        antMan.ongoing()
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

        self.location.addCard(mistyKnight3, self.player0)
        antMan.ongoing()
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2+4)
        self.assertTrue(antMan.ongoingTriggered)

        self.location.triggerOnReveal(mistyKnight3)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2+2+4)

        self.location.removeCard(mistyKnight1, self.player0.playerIdx)
        antMan.ongoing()
        self.assertEqual(self.location.getAmountOfCards(self.player0.playerIdx), 3)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

    def test_starLordNotTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(starLord, self.player0)
        self.location.triggerOnReveal(mistyKnight)
        self.location.triggerOnReveal(starLord)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2)

    def test_starLordTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(starLord, self.player1)
        self.location.triggerOnReveal(mistyKnight)
        self.location.triggerOnReveal(starLord)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2)
        self.assertEqual(self.location.getTotalPower(self.player1.playerIdx), 5)

    def test_elektra(self):
        mistyKnight = Card.MistyKnight()
        theThing = Card.TheThing()
        elektra = Card.Elektra()

        # when cards are not revealed, no cards are removed
        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(theThing, self.player0)
        self.location.addCard(elektra, self.player1)
        self.assertEqual(self.location.triggerOnReveal(elektra), None)
        self.assertEqual(self.location.getAmountOfCards(self.player0.playerIdx), 2)

        # reveal the two opposing cards, make sure misty knight is removed
        self.location.triggerOnReveal(mistyKnight)
        self.location.triggerOnReveal(theThing)
        removedCard = self.location.triggerOnReveal(elektra)
        self.assertEqual(removedCard, mistyKnight)
        self.assertEqual(self.location.getAmountOfCards(self.player0.playerIdx), 1)

    
    def test_yellowjacket(self):
        revealedMistyKnight = Card.MistyKnight()
        unrevealedMistyKnight = Card.MistyKnight()
        opposingMistyKnight = Card.MistyKnight()
        yellowjacket = Card.Yellowjacket()

        self.location.addCard(revealedMistyKnight, self.player0)
        self.location.triggerOnReveal(revealedMistyKnight)
        self.location.addCard(unrevealedMistyKnight, self.player0)
        self.location.addCard(opposingMistyKnight, self.player1)
        self.location.addCard(yellowjacket, self.player0)
        self.location.triggerOnReveal(opposingMistyKnight)
        self.location.triggerOnReveal(yellowjacket)
        self.location.triggerOnReveal(unrevealedMistyKnight)
        self.assertEqual(self.location.getTotalPower(self.player0.playerIdx), 2+2+1)
        self.assertEqual(self.location.getTotalPower(self.player1.playerIdx), 2)

        self.assertEqual(revealedMistyKnight.power, 1)
        self.assertEqual(unrevealedMistyKnight.power, 2)
        self.assertEqual(yellowjacket.power, 2)


    def test_mantisTrigger(self):
        mistyKnight = Card.MistyKnight()
        mantis = Card.Mantis()
        self.player1.deck = Deck.Deck(["mistyKnight", "antMan"])

        prevHandSize = len(self.player1.hand)
        self.location.addCard(mistyKnight, self.player0)
        self.location.addCard(mantis, self.player1)
        self.location.triggerOnReveal(mistyKnight)
        self.location.triggerOnReveal(mantis)
        self.assertEqual(len(self.player1.hand), prevHandSize + 1)
    
    def test_mantisTrigger(self):
        mantis = Card.Mantis()
        self.player1.deck = Deck.Deck(["mistyKnight", "antMan"])

        prevHandSize = self.player1.hand.getNumCards()
        self.location.addCard(mantis, self.player1)
        self.location.triggerOnReveal(mantis)
        self.assertEqual(self.player1.hand.getNumCards(), prevHandSize)
        


if __name__ == "__main__":
    unittest.main()