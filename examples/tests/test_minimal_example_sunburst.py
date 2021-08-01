#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import matplotlib

matplotlib.use("AGG")


class TestExample(unittest.TestCase):
    def test_all(self):
        from .. import minimal_example_sunburst


if __name__ == "__main__":
    unittest.main()
