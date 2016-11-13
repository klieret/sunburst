#!/usr/bin/env python3

import sys
import os.path
import matplotlib
if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path
import random

fig, ax = plt.subplots()

# set up some data

paths = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 222 "
                                 "1111 1112 1121".split(" ")]
pathvalues = {path: random.randrange(1, 100) for path in paths}

# do the magic

hp = HierarchicalPie(pathvalues, ax)

# set plot attributes

hp.plot(setup_axes=True)
ax.set_title('Example HPie')

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')
if len(sys.argv) == 1 or "debug" not in sys.argv:
    plt.show()