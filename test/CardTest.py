import unittest

import Card
import Location

class TestCards(unittest.TestCase):

    def setUp(self) -> None:
        self.location = Location.RuinsLocation(0)

    def test_tooManyCards(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        mistyKnight3 = Card.MistyKnight()
        mistyKnight4 = Card.MistyKnight()
        mistyKnight5 = Card.MistyKnight()

        self.location.addCard(mistyKnight1, 0)
        self.location.addCard(mistyKnight2, 0)
        self.location.addCard(mistyKnight3, 0)
        self.location.addCard(mistyKnight4, 0)
        with self.assertRaises(ValueError):
            self.location.addCard(mistyKnight5, 0)
    
    def test_plainCards(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        shocker = Card.Shocker()
        cyclops = Card.Cyclops()

        self.location.addCard(mistyKnight1, 0)
        self.location.addCard(mistyKnight2, 0)
        self.assertEqual(self.location.getTotalPower(0), 2+2)

        self.location.addCard(shocker, 1)
        self.location.addCard(cyclops, 1)
        self.assertEqual(self.location.getTotalPower(1), 3+4)
        self.assertEqual(self.location.getTotalPower(0), 2+2)
        
    
    def test_antMan(self):
        mistyKnight1 = Card.MistyKnight()
        mistyKnight2 = Card.MistyKnight()
        mistyKnight3 = Card.MistyKnight()
        antMan = Card.AntMan()

        self.location.addCard(mistyKnight1, 0)
        self.location.addCard(mistyKnight2, 0)
        self.location.addCard(antMan, 0)
        antMan.ongoing()
        self.assertEqual(self.location.getTotalPower(0), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

        self.location.addCard(mistyKnight3, 0)
        antMan.ongoing()
        self.assertEqual(self.location.getTotalPower(0), 2+2+2+4)
        self.assertTrue(antMan.ongoingTriggered)

        self.location.removeCard(mistyKnight1, 0)
        antMan.ongoing()
        self.assertEqual(self.location.getAmountOfCards(0), 3)
        self.assertEqual(self.location.getTotalPower(0), 2+2+1)
        self.assertFalse(antMan.ongoingTriggered)

    def test_starLordNotTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, 0)
        self.location.addCard(starLord, 0)
        starLord.onReveal()
        self.assertEqual(self.location.getTotalPower(0), 2+2)

    def test_starLordTrigger(self):
        starLord = Card.StarLord()
        mistyKnight = Card.MistyKnight()

        self.location.addCard(mistyKnight, 0)
        self.location.addCard(starLord, 1)
        starLord.onReveal()
        self.assertEqual(self.location.getTotalPower(0), 2)
        self.assertEqual(self.location.getTotalPower(1), 5)

    def test_elektra(self):
        mistyKnight = Card.MistyKnight()
        abomination = Card.Abomination()
        elektra = Card.Elektra()

        # when cards are not revealed, no cards are removed
        self.location.addCard(mistyKnight, 0)
        self.location.addCard(abomination, 0)
        self.location.addCard(elektra, 1)
        self.assertEqual(self.location.triggerOnReveal(elektra), None)
        self.assertEqual(self.location.getAmountOfCards(0), 2)

        # reveal the to opposing cards
        self.location.triggerOnReveal(mistyKnight)
        self.location.triggerOnReveal(abomination)
        removedCard = self.location.triggerOnReveal(elektra)
        self.assertEqual(removedCard, mistyKnight)
        self.assertEqual(self.location.getAmountOfCards(0), 1)

    
    def test_Yellowjacket(self):
        revealedMistyKnight = Card.MistyKnight()
        unrevealedMistyKnight = Card.MistyKnight()
        opposingMistyKnight = Card.MistyKnight()
        yellowjacket = Card.Yellowjacket()

        self.location.addCard(revealedMistyKnight, 0)
        revealedMistyKnight.onReveal()
        self.location.addCard(unrevealedMistyKnight, 0)
        self.location.addCard(opposingMistyKnight, 1)
        self.location.addCard(yellowjacket, 0)
        yellowjacket.onReveal()
        unrevealedMistyKnight.onReveal()

        self.assertEqual(self.location.getTotalPower(0), 2+2+1)
        self.assertEqual(self.location.getTotalPower(1), 2)

        self.assertEqual(revealedMistyKnight.power, 1)
        self.assertEqual(unrevealedMistyKnight.power, 2)
        self.assertEqual(yellowjacket.power, 2)
        


if __name__ == "__main__":
    unittest.main()