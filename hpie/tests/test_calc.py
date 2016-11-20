#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..path import charvalues_to_pathvalues
from ..calc import *
from typing import List

# Abbreviations:
#    hc: hand-calculated
#    pv: path values, i.e. Dict[Path: float]


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


class CalcTest(unittest.TestCase):

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
        self.hc_complete_pv = charvalues_to_pathvalues({
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

        self.hc_complete_pv_summed = charvalues_to_pathvalues({
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

        self.assertEqual(self.hc_complete_pv, self.hc_complete_pv_summed)

        self.hc_structurized_paths = stringstruct_to_pathstruct([
            [[""]],
            [["1", "2"]],
            [["11", "12", "13"], ["21"]],
            [["111", "112", "113"], ["121", "122"], ["211"]],
            [["1111", "1112"], ["1121"]]
        ])

    def test_complete_paths(self):
        self.assertEqual(complete_paths(sorted(self.pathvalues.keys())),
                         sorted(self.hc_complete_pv))

    def test_complete(self):
        # for better debugging: loop
        calculated = complete_pv(self.pathvalues)

        # chances are we forgot some keys in hand_calculated:
        for key in calculated.keys():
            with self.subTest(key=key):
                self.assertIn(key, self.hc_complete_pv)

        # we verified that hand_calculated has more or equally many keys as
        # calculated now check all values (thereby also checking that the
        # keys are exactly equal):
        for key in self.hc_complete_pv.keys():
            with self.subTest(key=key):
                self.assertAlmostEqual(calculated[key],
                                       self.hc_complete_pv[key])

    def test_structurize(self):
        calculated = structurize(list(self.hc_complete_pv.keys()))
        self.assertEqual(pathstruct_no_order(calculated),
                         pathstruct_no_order(self.hc_structurized_paths))

    def test_calculate_angles(self):
        angles_dict = calculate_angles(self.hc_structurized_paths,
                                       self.hc_complete_pv)
        for path, angles in angles_dict.items():
            with self.subTest(path=path):
                hc_angle_diff = self.hc_complete_pv[path] / \
                                self.hc_complete_pv[Path(())] * 360.
                theta1 = angles.theta1
                theta2 = angles.theta2
                self.assertAlmostEqual(hc_angle_diff,
                                       angles.theta2 - angles.theta1)
                for ancestor in path.ancestors():
                    # compare the computed angles, to avoid issues with
                    # floating point precision. This should be exact.
                    self.assertLessEqual(angles_dict[ancestor].theta1, theta1)
                    self.assertLessEqual(theta1, theta2)
                    self.assertLessEqual(theta2, angles_dict[ancestor].theta2)
