
class Card(object):

    def __init__(self, cost, power, name):
        self.name = name
        self.cost = cost
        self.power = power

    def __str__(self) -> str:
        return f"{self.name} (cost: {self.cost}, power: {self.power})"

    def ongoing(self):
        return None

    def onReveal(self):
        return None

class MistyKnight(Card):
    
    def __init__(self):
        super(MistyKnight, self).__init__(1, 2, "Misty Knight")
        

class Shocker(Card):

    def __init__(self):
        super(Shocker, self).__init__(2, 3, "Shocker")


class Cyclops(Card):

    def __init__(self):
        super(Cyclops, self).__init__(3, 4, "Cyclops")


class Abomination(Card):

    def __init__(self):
        super(Abomination, self).__init__(4, 6, "Abomination")