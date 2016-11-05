#!/usr/bin/env python3
# -*- coding: utf8 -*-

from path import Path, paths2dot
import random
import os.path

numbering = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 "
                                     "222 1111 1112 1121".split(" ")]

with open("example_numbering.gv", "w") as out:
    out.writelines(paths2dot(numbering))

numbering_pv = {path: random.uniform(1, 100) for path in numbering}
