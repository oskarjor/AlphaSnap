DECKSIZE = 12
NUM_LOCATIONS = 3

TURN_STAGES = {
    "BEFORE_TURN": 0,
    "DURING_TURN": 1,
    "AFTER_TURN": 2,
}

SAMPLE_DECK = ["Wasp", "Misty Knight", "Shocker",
               "Star Lord", "Cyclops", "Groot", "The Thing"]

VERBOSE = 2

PATH_TO_IMAGES = "images/"
PATH_TO_CHARACHTER_STATS = "characters/"
CURRENT_CHARACTER_SNAPSHOT = "characters_10_26_23.json"

# EVENTTYPES

# CARD ACTIONS


def CARD_PLAYED(player, card, location): return [
    "cardPlayed", player, card, location]


def CARD_REVEALED(player, card, location): return [
    "cardRevealed", player, card, location]


def CARD_MOVED(player, card, fromLocation, toLocation): return [
    "cardMoved", player, card, fromLocation, toLocation]


def CARD_DISCARDED(player, card, location): return [
    "cardDiscarded", player, card, location]


def CARD_DESTROYED(player, card, location): return [
    "cardDestroyed", player, card, location]

# LOCATION ACTIONS


def LOCATION_REVEALED(location): return ["locationRevealed", location]
def LOCATION_ABILTITY_TRIGGERED(location): return [
    "locationAbilityTriggered", location]

# GAME ACTIONS


def TURN_STARTED(): return ["turnStarted"]
def TURN_ENDED(): return ["turnEnded"]
def GAME_STARTED(): return ["gameStarted"]
def GAME_ENDED(result): return ["gameEnded", result]


if __name__ == "__main__":
    print(LOCATION_REVEALED)
