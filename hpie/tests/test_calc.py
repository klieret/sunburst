#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..path import Path, charvalues_to_pathvalues
from ..calc import complete, structurize
from typing import List


def stringstruct_to_pathstruct(stringstruct: List[List[List[str]]]):
    return [
              [
                  [Path(tuple(string)) for string in lst]
                  for lst in lstlst
              ]
              for lstlst in stringstruct
           ]


def pathstruct_no_order(pathstruct: List[List[List[Path]]]):
    return frozenset([frozenset([frozenset(lst) for lst in lstlst]) for lstlst
                      in pathstruct])


class HpieTest(unittest.TestCase):

    def setUp(self):
        self.pathvalues = charvalues_to_pathvalues({
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

        # hand calculated
        self.hand_calculate_complete = charvalues_to_pathvalues({
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

        self.hand_calculate_complete_summed = charvalues_to_pathvalues({
                '': 572.,
                '1': 500.,
                '11': 303.,
                '111': 206.,
                '1111': 15.,
                '1112': 99.,
                '112': 70.,
                '1121': 70.,
                '113': 27.,
                '12': 123.,
                '121': 43.,
                '122': 29.,
                '13': 69.,
                '2': 72.,
                '21': 43.,
                '211': 43.})

        self.assertEqual(self.hand_calculate_complete,
                         self.hand_calculate_complete_summed)

        self.hand_calculated_structurized = stringstruct_to_pathstruct([
            [[""]],
            [["1", "2"]],
            [["11", "12", "13"], ["21"]],
            [["111", "112", "113"], ["121", "122"], ["211"]],
            [["1111", "1112"], ["1121"]]
        ])

    def test_complete(self):
        # for better debugging: loop
        calculated = complete(self.pathvalues)

        # chances are we forgot some keys in hand_calculated:
        for key in calculated.keys():
            with self.subTest(key=key):
                self.assertIn(key, self.hand_calculate_complete)

        # we verified that hand_calculated has more or equally many keys as
        # calculated now check all values (thereby also checking that the
        # keys are exactly equal):
        for key in self.hand_calculate_complete.keys():
            with self.subTest(key=key):
                self.assertEqual(calculated[key],
                                 self.hand_calculate_complete[key])

    def test_structurize(self):
        calculated = structurize(list(self.hand_calculate_complete.keys()))
        self.assertEqual(pathstruct_no_order(calculated),
                         pathstruct_no_order(self.hand_calculated_structurized))

