#!/usr/bin/env python3

from path import Path
import random

inpt = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 222 1111 1112 1121".split(" ")]
pathtimes = {path: random.uniform(1,100) for path in inpt}