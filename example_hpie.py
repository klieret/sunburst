#!/usr/bin/env python3

import example_paths
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie

e_pathtimes = example_paths.pathvalues

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_ylim([-2, 2])
ax.set_xlim([-2, 2])

hp = HierarchicalPie(e_pathtimes, ax)
hp.plot()

plt.show()