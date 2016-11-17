#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..path import Path


class PathTest(unittest.TestCase):

    def setUp(self):
        self.paths = {
            "empty": Path(()),
            "triple": Path(("a", "b", "c")),
            "unicode": Path(("東京", ))
        }

    def test_length(self):
        self.assertEqual(len(self.paths["empty"]), 0)
        self.assertEqual(len(self.paths["triple"]), 3)
        self.assertEqual(len(self.paths["unicode"]), 1)

    def test_getitem(self):
        for _, path in self.paths.items():
            for i in range(len(path)):
                self.assertIsInstance(path[i], Path)

    def test_slice(self):
        for _, path in self.paths.items():
            for i in range(len(path)):
                for j in range(len(path)):
                    self.assertIsInstance(path[i:j], Path)
                    if i > j:
                        self.assertEqual(path[i:j], Path(()))
                    if i == j - 1:
                        self.assertEqual(path[i:j], path[i])
                    if i == 0 and j == len(path):
                        self.assertEqual(path[i:j], path)

    def test_parent(self):
        self.assertEqual(self.paths["empty"].parent(), Path(()))
        self.assertEqual(self.paths["unicode"].parent(), Path(()))
        self.assertEqual(self.paths["triple"].parent(), Path(("a", "b")))

    def test_ancestors(self):
        for path in self.paths.values():
            self.assertEqual(len(path.ancestors()), len(path) + 1)

if __name__ == '__main__':
    unittest.main()

