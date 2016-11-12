#!/usr/bin/env python3

import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path
import csv

fig, ax = plt.subplots()

# read data

pathvalues = {}
with open("file_sizes.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        print(row)
        if not len(row) == 2:
            continue
        pathvalues[Path(row[1].split('/'))] = float(row[0])

# do the magic

hp = HierarchicalPie(pathvalues, ax)

# set plot attributes

hp.plot()
ax.autoscale()
ax.set_aspect("equal")
ax.autoscale_view(True, True, True)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.margins(x=0.1, y=0.1)
ax.set_title('Example HPie')

plt.show()