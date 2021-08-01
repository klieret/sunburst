#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from sunburst.path import charvalues_to_pv
from sunburst.calc import *
from typing import List

# Abbreviations:
#    hc: hand-calculated
#    pv: path values, i.e. Dict[Path: float]


def stringstruct_to_pathstruct(stringstruct: List[List[List[str]]]):
    return [
        [[Path(tuple(string)) for string in lst] for lst in lstlst]
        for lstlst in stringstruct
    ]


def pathstruct_no_order(pathstruct: List[List[List[Path]]]):
    return frozenset(
        [frozenset([frozenset(lst) for lst in lstlst]) for lstlst in pathstruct]
    )


class CalcTest(unittest.TestCase):
    def setUp(self):
        self.pathvalues = charvalues_to_pv(
            {
                "1": 5.0,
                "111": 92.0,
                "1111": 15.0,
                "1112": 99.0,
                "112": 0.0,
                "1121": 70.0,
                "113": 27.0,
                "12": 51.0,
                "121": 43.0,
                "122": 29.0,
                "13": 69.0,
                "2": 29.0,
                "211": 43.0,
            }
        )

        # hand calculated
        self.hc_complete_pv = charvalues_to_pv(
            {
                "": 5
                + 92
                + 15
                + 99
                + 0
                + 70
                + 27
                + 51
                + 43
                + 29
                + 69
                + 29
                + 43.0,
                "1": 5 + 92 + 15 + 99 + 0 + 70 + 27 + 51 + 43 + 29 + 69.0,
                "11": 92 + 15 + 99 + 70 + 27.0,
                "111": 92 + 15 + 99.0,
                "1111": 15.0,
                "1112": 99.0,
                "112": 70.0,
                "1121": 70.0,
                "113": 27.0,
                "12": 51 + 43 + 29.0,
                "121": 43.0,
                "122": 29.0,
                "13": 69.0,
                "2": 29 + 43.0,
                "21": 43.0,
                "211": 43.0,
            }
        )

        self.hc_complete_pv_summed = charvalues_to_pv(
            {
                "": 572.0,
                "1": 500.0,
                "11": 303.0,
                "111": 206.0,
                "1111": 15.0,
                "1112": 99.0,
                "112": 70.0,
                "1121": 70.0,
                "113": 27.0,
                "12": 123.0,
                "121": 43.0,
                "122": 29.0,
                "13": 69.0,
                "2": 72.0,
                "21": 43.0,
                "211": 43.0,
            }
        )

        self.assertEqual(self.hc_complete_pv, self.hc_complete_pv_summed)

        self.hc_structurized_paths = stringstruct_to_pathstruct(
            [
                [[""]],
                [["1", "2"]],
                [["11", "12", "13"], ["21"]],
                [["111", "112", "113"], ["121", "122"], ["211"]],
                [["1111", "1112"], ["1121"]],
            ]
        )

    def test_complete_paths(self):
        self.assertEqual(
            complete_paths(sorted(self.pathvalues.keys())),
            sorted(self.hc_complete_pv),
        )

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
                self.assertAlmostEqual(
                    calculated[key], self.hc_complete_pv[key]
                )

    def test_structurize(self):
        calculated = structure_paths(list(self.hc_complete_pv.keys()))
        self.assertEqual(
            pathstruct_no_order(calculated),
            pathstruct_no_order(self.hc_structurized_paths),
        )

    def test_calculate_angles(self):
        angles_dict = calculate_angles(
            self.hc_structurized_paths, self.hc_complete_pv
        )
        for path, angles in angles_dict.items():
            with self.subTest(path=path):
                hc_angle_diff = (
                    self.hc_complete_pv[path]
                    / self.hc_complete_pv[Path(())]
                    * 360.0
                )
                theta1 = angles.theta1
                theta2 = angles.theta2
                self.assertAlmostEqual(
                    hc_angle_diff, angles.theta2 - angles.theta1
                )
                for ancestor in path.ancestors():
                    # compare the computed angles, to avoid issues with
                    # floating point precision. This should be exact.
                    self.assertLessEqual(angles_dict[ancestor].theta1, theta1)
                    self.assertLessEqual(theta1, theta2)
                    self.assertLessEqual(theta2, angles_dict[ancestor].theta2)
