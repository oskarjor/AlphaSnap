import random

from marvelsnap import Location, Player, utils


class Board(object):

    def __init__(self, locations: list[Location.Location] | None = None) -> None:
        if not locations:
            self.locations = [None, None, None]
        else:
            self.locations = locations

    def getLocations(self):
        return self.locations

    def createLocation(self, idx: int, locationName: str) -> None:
        if (utils.GLOBAL_CONSTANTS.VERBOSE > 1):
            print(f"Location {idx}: {locationName}")
        LOCATION_DICT = Location.getFlatLocationDict()
        self.locations[idx] = LOCATION_DICT[locationName](idx)

    def setupLocations(self, locations: list[str] = None) -> None:
        if locations == None:
            LOCATION_DICT = Location.getFlatLocationDict()
            locations = random.sample(list(LOCATION_DICT.keys()), 3)
        for i, locName in enumerate(locations):
            self.createLocation(i, locName)

    def playerIsStarting(self, player: Player.Player):
        isPlayerWinning = self.playerIsWinning(player=player)
        if (isPlayerWinning == 1):
            return 1
        elif (isPlayerWinning == -1):
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
                if (selfPower > opposingPower):
                    wonLocations += 1
                if (selfPower < opposingPower):
                    lostLocations += 1
        if (wonLocations > lostLocations):
            return 1
        if (wonLocations < lostLocations):
            return -1
        if (wonLocations == lostLocations):
            if (sumSelfPower > sumOpposingPower):
                return 1
            if (sumSelfPower < sumOpposingPower):
                return -1
            if (sumSelfPower == sumOpposingPower):
                return 0
