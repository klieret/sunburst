#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import matplotlib
from os.path import dirname, join, realpath, exists

matplotlib.use("AGG")

file_size_data_file = realpath(
    join(dirname(__file__), "..", "data", "file_sizes.txt")
)


@unittest.skipUnless(exists(file_size_data_file), "Data is missing.")
class TestExample(unittest.TestCase):
    def test_all(self):
        from .. import disk_usage_exploded


if __name__ == "__main__":
    unittest.main()
