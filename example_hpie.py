#!/usr/bin/env python3

import example_paths
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie

e_pathtimes = example_paths.pathvalues

fig, ax = plt.subplots()
hp = HierarchicalPie(e_pathtimes, ax)
hp.plot()
ax.autoscale()
ax.set_aspect("equal")
ax.autoscale_view(True, True, True)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.margins(x=0.1, y=0.1)
ax.set_title('Example HPie')

plt.show()