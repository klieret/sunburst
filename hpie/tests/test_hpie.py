#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..path import Path
from ..hpie import complete

class HpieTest(unittest.TestCase):

    def setUp(self):
        self.pathvalues = {Path(('1',)): 0.,
                           Path(('1', '1', '1')): 92.,
                           Path(('1', '1', '1', '1')): 15.,
                           Path(('1', '1', '1', '2')): 99.,
                           Path(('1', '1', '2')): 0.,
                           Path(('1', '1', '2', '1')): 70.,
                           Path(('1', '1', '3')): 27.,
                           Path(('1', '2')): 51.,
                           Path(('1', '2', '1')): 43.,
                           Path(('1', '2', '2')): 29.,
                           Path(('1', '3')): 69.,
                           Path(('2',)): 29.,
                           Path(('2', '1', '1')): 43.}

    def test_complete(self):
        # hand calculated
        hand_calculated = {Path(()): 0+92+15+99+0+70+27+51+43+29+69+29+43.,
                Path(('1',)): 0+92+15+99+0+70+27+51+43+29+69.,
                Path(('1', '1',)): 92+15+99+70+27.,
                Path(('1', '1', '1')): 92+15+99.,
                Path(('1', '1', '1', '1')): 15.,
                Path(('1', '1', '1', '2')): 99.,
                Path(('1', '1', '2')): 70.,
                Path(('1', '1', '2', '1')): 70.,
                Path(('1', '1', '3')): 27.,
                Path(('1', '2')): 51+43+29.,
                Path(('1', '2', '1')): 43.,
                Path(('1', '2', '2')): 29.,
                Path(('1', '3')): 69.,
                Path(('2',)): 29+43.,
                Path(('2', '1',)): 43.,
                Path(('2', '1', '1')): 43.}

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