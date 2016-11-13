#!/usr/bin/env python3

import sys
import os.path
import matplotlib
if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path

fig, ax = plt.subplots()

# set up some random data

data = {
    Path(('lorem', )): 36.12,  # note the ','
    Path(('ipsum', 'eirmod', 'dolor')): 94.4,
    Path(('lorem', 'sadipscing', 'dolor')): 44.32,
    Path(('lorem', 'sadipscing', 'lorem')): 37.15,
    Path(('lorem', 'eirmod', 'lorem')): 45.65,
    Path(('ipsum', 'eirmod')): 29.34,
    Path(('lorem', 'eirmod')): 11.12,
    Path(('lorem', 'sadipscing', 'nonumy')): 23.98,
    Path(('ipsum',)): 40.45,
    Path(('lorem', 'sadipscing')): 79.67,
}

# do the magic

hp = HierarchicalPie(data, ax)

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
