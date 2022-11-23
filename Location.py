from Card import Card

class Location(object):

    def __init__(self, name: str, idx: int, freeSpaces: list[int, int], desc: str) -> None:
        self.name = name
        self.idx = idx
        self.freeSpaces = freeSpaces
        self.cards = None
        self.totalEnergy = 0
        self.desc = desc

    def __str__(self) -> str:
        return f"{self.name} ({self.idx})"

    def isPlayable(self, playerIdx) -> bool:
        if(self.freeSpaces[playerIdx] <= 0):
            print("This location is full")
            return False
        return True
    
    def addCard(self, card: Card, playerIdx: int):
        pass

class RuinsLocation(Location):

    def __init__(self, idx: int):
        super(RuinsLocation, self).__init__(name="Ruins", idx=idx, freeSpaces=[4, 4], desc="A ruined land")
