#!/usr/bin/env python3

from path import Path, paths2dot
import random

paths = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 222 "
                                 "1111 1112 1121".split(" ")]

with open("example_paths.gv", "w") as out:
    out.writelines(paths2dot(paths))

pathvalues = {path: random.uniform(1, 100) for path in paths}
