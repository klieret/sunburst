#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from sunburst.path import Path, charvalues_to_pv


class PathTest(unittest.TestCase):
    def setUp(self):
        self.paths = {
            "empty": Path(()),
            "triple": Path(("a", "b", "c")),
            "unicode": Path(("東京",)),
        }

    def test_length(self):
        self.assertEqual(len(self.paths["empty"]), 0)
        self.assertEqual(len(self.paths["triple"]), 3)
        self.assertEqual(len(self.paths["unicode"]), 1)

    def test_init(self):
        self.assertEqual(Path(""), self.paths["empty"])
        self.assertEqual(Path("abc"), self.paths["triple"])
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual(len(Path("a" * i)), i)
                self.assertEqual(len(Path(["a"] * i)), i)
                self.assertEqual(len(Path(("a",) * i)), i)
                self.assertEqual(len(Path(("",)) * i), i)

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
            ancestors = path.ancestors()
            self.assertEqual(len(ancestors), len(path) + 1)
            self.assertIn(Path(()), ancestors)
            self.assertIn(path, ancestors)
            self.assertIn(path.parent(), ancestors)

    def test_startswith(self):
        for path in self.paths.values():
            self.assertTrue(path.startswith(Path(())))
            for ancestor in path.ancestors():
                self.assertTrue(path.startswith(ancestor))


class TestConversions(unittest.TestCase):
    def test_charvalues_to_pathvalues(self):
        charvalues = {"123": 1.0, "": 2.0, "1": 3.0}
        pathvalues = {Path("123"): 1.0, Path(()): 2.0, Path("1"): 3.0}
        self.assertEqual(charvalues_to_pv(charvalues), pathvalues)


if __name__ == "__main__":
    unittest.main()
