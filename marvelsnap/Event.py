from typing import TYPE_CHECKING

from enum import Enum
if TYPE_CHECKING:
    import Card
    import Location
    import Player


class Event(object):

    def __init__(self, category: str) -> None:
        self.category = category


class EventCategories(Enum):
    CARD_EVENT = 1
    LOCATION_EVENT = 2
    GAME_EVENT = 3


class LocationEventCategories(Enum):
    LOCATION_REVEALED = 1
    LOCATION_ABILTITY_TRIGGERED = 2


class CardEventCategories(Enum):
    CARD_PLAYED = 1
    CARD_REVEALED = 2
    CARD_MOVED = 3
    CARD_DISCARDED = 4
    CARD_DESTROYED = 5


class GameEventCateogories(Enum):
    TURN_STARTED = 1
    TURN_ENDED = 2
    GAME_STARTED = 3
    GAME_ENDED = 4


class CardEvent(Event):

    def __init__(self, player, card, location) -> None:
        super().__init__(EventCategories.CARD_EVENT)
        self.player = player
        self.card = card
        self.location = location

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - P{self.player} (Card: {self.card} -> Loc: {self.location})"


class CardPlayed(CardEvent):

    def __init__(self, player, card, location) -> None:
        super().__init__(player, card, location)
        self.sub_category = CardEventCategories.CARD_PLAYED


class CardRevealed(CardEvent):

    def __init__(self, player, card, location) -> None:
        super().__init__(player, card, location)
        self.sub_category = CardEventCategories.CARD_REVEALED


class CardMoved(CardEvent):

    def __init__(self, player, card, location) -> None:
        super().__init__(player, card, location)
        self.sub_category = CardEventCategories.CARD_MOVED


class CardDiscarded(CardEvent):

    def __init__(self, player, card, location) -> None:
        super().__init__(player, card, location)
        self.sub_category = CardEventCategories.CARD_DISCARDED


class CardDestroyed(CardEvent):

    def __init__(self, player, card, location) -> None:
        super().__init__(player, card, location)
        self.sub_category = CardEventCategories.CARD_DESTROYED


class LocationEvent(Event):

    def __init__(self, location) -> None:
        super().__init__(EventCategories.LOCATION_EVENT)
        self.location = location

    def __str__(self) -> str:
        return f"{self.location}: {self.__class__.__name__}"


class LocationRevealed(LocationEvent):

    def __init__(self, location) -> None:
        super().__init__(location)
        self.sub_category = LocationEventCategories.LOCATION_REVEALED


class LocationAbilityTriggered(LocationEvent):

    def __init__(self, location) -> None:
        super().__init__(location)
        self.sub_category = LocationEventCategories.LOCATION_ABILTITY_TRIGGERED


class GameEvent(Event):

    def __init__(self) -> None:
        super().__init__(EventCategories.GAME_EVENT)

    def __str__(self) -> str:
        return self.__class__.__name__


class TurnStarted(GameEvent):

    def __init__(self) -> None:
        super().__init__()
        self.sub_category = GameEventCateogories.TURN_STARTED


class TurnEnded(GameEvent):

    def __init__(self) -> None:
        super().__init__()
        self.sub_category = GameEventCateogories.TURN_ENDED


class GameStarted(GameEvent):

    def __init__(self) -> None:
        super().__init__()
        self.sub_category = GameEventCateogories.GAME_STARTED


class GameEnded(GameEvent):

    def __init__(self) -> None:
        super().__init__()
        self.sub_category = GameEventCateogories.GAME_ENDED
