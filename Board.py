from CONSTANTS import LOCATION_DICT
import random
import Player

class Board(object):

    def __init__(self) -> None:
        self.locations = [None, None, None]

    def createLocation(self, idx: int) -> None:
        currentLocation = random.choice(list(LOCATION_DICT.keys()))
        #print(f"Location {idx}: {currentLocation}")
        self.locations[idx] = LOCATION_DICT[currentLocation](idx)
    
    def setupLocations(self) -> None:
        #print("Selecting locations")
        for i in range(3):
            self.createLocation(i)

    def playerIsStarting(self, player: Player.Player):
        isPlayerWinning = self.playerIsWinning(player=player)
        if(isPlayerWinning == 1):
            return 1
        elif(isPlayerWinning == -1):
            return 0
        return random.randint(0, 1)


    def playerIsWinning(self, player: Player.Player):
        sumSelfPower = 0
        sumOpposingPower = 0
        wonLocations = 0
        lostLocations = 0
        for location in self.locations:
            if location != None:
                selfPower = location.getTotalPower(player.playerIdx)
                sumSelfPower += selfPower
                opposingPower = location.getTotalPower(1 - player.playerIdx)
                sumOpposingPower += opposingPower
                if(selfPower > opposingPower):
                    wonLocations += 1
                if(selfPower < opposingPower):
                    lostLocations += 1
        if(wonLocations > lostLocations):
            return 1
        if(wonLocations < lostLocations):
            return -1
        if(wonLocations == lostLocations):
            if(sumSelfPower > sumOpposingPower):
                return 1
            if(sumSelfPower < sumOpposingPower):
                return -1
            if(sumSelfPower == sumOpposingPower):
                return 0
            
