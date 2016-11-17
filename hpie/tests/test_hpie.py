#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..path import Path
from ..hpie import complete
from typing import Dict


def strinvalues_to_pathvalues(stringvalues: Dict[str, float]):
    return {Path(tuple(item)): value for item, value in stringvalues.items()}


class HpieTest(unittest.TestCase):

    def setUp(self):
        self.pathvalues = strinvalues_to_pathvalues({
                           '1': 5.,
                           '111': 92.,
                           '1111': 15.,
                           '1112': 99.,
                           '112': 0.,
                           '1121': 70.,
                           '113': 27.,
                           '12': 51.,
                           '121': 43.,
                           '122': 29.,
                           '13': 69.,
                           '2': 29.,
                           '211': 43.})

    def test_complete(self):
        # hand calculated
        hand_calculated = strinvalues_to_pathvalues({
                '': 5+92+15+99+0+70+27+51+43+29+69+29+43.,
                '1': 5+92+15+99+0+70+27+51+43+29+69.,
                '11': 92+15+99+70+27.,
                '111': 92+15+99.,
                '1111': 15.,
                '1112': 99.,
                '112': 70.,
                '1121': 70.,
                '113': 27.,
                '12': 51+43+29.,
                '121': 43.,
                '122': 29.,
                '13': 69.,
                '2': 29+43.,
                '21': 43.,
                '211': 43.})

        # for better debugging: loop
        calculated = complete(self.pathvalues)

        # chances are we forgot some keys in hand_calculated:
        for key in calculated.keys():
            with self.subTest(key=key):
                self.assertIn(key, hand_calculated)

        # we verified that hand_calculated has more or equally many keys as
        # calculated now check all values (thereby also checking that the
        # keys are exactly equal):
        for key in hand_calculated.keys():
            with self.subTest(key=key):
                self.assertEqual(calculated[key], hand_calculated[key])
