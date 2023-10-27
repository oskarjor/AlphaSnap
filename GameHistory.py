class GameHistory(object):

    def __init__(self) -> None:
        # a dict of everything that has happened during the game
        # Format
        # {
        #   turn : [event_1, event_2, event_3, event_4, ...]
        #   turn : [event_1, event_2, event_3, event_4, ...]
        #   turn : [event_1, event_2, event_3, event_4, ...]
        # }
        # event_i = [eventType, ...]
        #
        # CARD ACTIONS:
        # eventType = cardPlayed                ->      turn : ["cardPlayed", player, card, location]       (check)
        # eventType = cardRevealed              ->      turn : ["cardRevealed", player, card, location]     (check)
        # eventType = cardMoved                 ->      turn : ["cardMoved", player, card, fromLocation, toLocation]
        # eventType = cardDestroyed             ->      turn : ["cardDestroyed", player, card, location]
        # eventType = cardDiscarded             ->      turn : ["cardDiscarded", player, card, location]
        #
        # LOCATION ACTIONS:
        # eventType = locationRevealed          ->      turn : ["locationRevealed", location]
        # eventType = locationAbilityTriggered  ->      turn : ["locationAbilityTriggered", location]
        #
        # GAME ACTIONS:
        # eventType = turnStart                 ->      turn : ["turnStarted"]       (check)
        # eventType = turnEnd                   ->      turn : ["turnEnded"]         (check)
        # eventType = gameStarted               ->      turn : ["gameStarted"]       (check)
        # eventType = gameEnded                 ->      turn : ["gameEnded", result] (check)
        self.history = {}
        self.current_turn = 0

    def addEvent(self, event: list, turn: int | None = None) -> None:
        if turn == None:
            turn = self.current_turn
        if turn in self.history:
            self.history[turn].append(event)
        else:
            self.history[turn] = [event]

    def updateTurn(self, turn: int) -> None:
        self.turn = turn

    def getLatestEventInGame(self, turn: int) -> list | None:
        while turn > 0:
            event = self.getLatestEventInTurn(turn=turn)
            if event != None:
                return event
            else:
                turn -= 1
        return None

    def getLatestEventInTurn(self, turn: int) -> list | None:
        turnHistory = self.getTurnHistory(turn=turn)
        if turnHistory:
            return turnHistory[-1]
        return None

    def getTurnHistory(self, turn: int) -> list | None:
        if turn in self.history:
            return self.history[turn]
        else:
            return None

    def getLatestEventOfTypeInGame(self, eventType: str) -> list | None:
        turn = self.current_turn
        while turn > 0:
            event = self.getLatestEventOfTypeInTurn(
                turn=turn, eventType=eventType)
            if event != None:
                return event
            else:
                turn -= 1
        return None

    def getLatestEventOfTypeInTurn(self, turn: int, eventType: str) -> list | None:
        turnHistory = self.getTurnHistory(turn=turn)
        if turnHistory == None:
            return None
        turnHistory.reverse()
        for event in turnHistory:
            if event[0] == eventType:
                return event
        return None


gameHistory = GameHistory()
