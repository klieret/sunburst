#!/usr/bin/env python3
# -*- coding: utf8 -*-

from hpie import Path, paths2dot

numbering = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 "
                                     "222 1111 1112 1121".split(" ")]

with open("example_numbering.gv", "w") as out:
    out.writelines(paths2dot(numbering))
