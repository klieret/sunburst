#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os.path
from sunburst import Path, paths2dot

numbering = [
    Path(tuple(a))
    for a in "1 2 12 13 111 112 113 121 122 211 221 "
    "222 1111 1112 1121".split(" ")
]

with open(
    os.path.join(
        os.path.dirname(__file__),
        "figures",
        "{}.gv".format(os.path.basename(__file__)),
    ),
    "w",
) as out:
    out.writelines(paths2dot(numbering))
