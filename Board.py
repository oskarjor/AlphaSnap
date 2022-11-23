from CONSTANTS import LOCATION_DICT
import random

class Board(object):

    def __init__(self) -> None:
        self.locations = [None, None, None]

    def createLocation(self, idx: int) -> None:
        currentLocation = random.choice(list(LOCATION_DICT.keys()))
        print(f"Location {idx}: {currentLocation}")
        self.locations[idx] = LOCATION_DICT[currentLocation](idx)
    
    def setupLocations(self) -> None:
        print("Selecting locations")
        for i in range(3):
            self.createLocation(i)
