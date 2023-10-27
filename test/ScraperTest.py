import unittest
import json
import os

import Card
import Location
import Player
import Game
import Board

import utils.GLOBAL_CONSTANTS as GLOBAL_CONSTANTS
from utils.utils import all_subclasses


class TestScraper(unittest.TestCase):

    def setUp(self) -> None:
        path = GLOBAL_CONSTANTS.PATH_TO_CHARACHTER_STATS + \
            GLOBAL_CONSTANTS.CURRENT_CHARACTER_SNAPSHOT
        path = os.path.abspath(path)
        with open(path) as json_file:
            self.data = json.load(json_file)
        sub = all_subclasses(Card.Card)
        self.implemented_card_names = []
        for s in sub:
            try:
                self.implemented_card_names.append(s().name.lower())
            except:
                pass

    def test_all_cards_implemented(self):
        unimplemented = 0
        unimplemented_names = []
        for key in self.data.keys():
            if key.lower() not in self.implemented_card_names:
                unimplemented += 1
                unimplemented_names.append(key)

        if unimplemented > 0:
            if GLOBAL_CONSTANTS.VERBOSE > 0:
                raise NotImplementedError(
                    f"{unimplemented_names} not implemented ({unimplemented})")
            else:
                raise NotImplementedError(
                    f"{unimplemented} cards not implemented")
