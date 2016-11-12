#!/usr/bin/env python3

import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path
import csv
import sys

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

hp = HierarchicalPie(pathvalues,
                     ax,
                     cmap=plt.get_cmap("hsv"),
                     plot_minimal_angle=0,
                     text_minimal_angle=1.5)

# Do not display values
hp.format_value_text = lambda value: None

# set plot attributes

hp.plot()
ax.autoscale()
ax.set_aspect("equal")
ax.autoscale_view(True, True, True)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.margins(x=0.1, y=0.1)
ax.set_title('Disk usage chart of this repository.\n'
             'Total size: {} bit'.format(int(hp._completed_pv[Path(("", ))])))
fig.set_size_inches(10, 10)

# a few command line options to display plot/save figure/do nothing:

if "debug" in sys.argv[1:]:
    pass
if "save" in sys.argv[1:]:
    fig.savefig("{}.png".format(__file__), dpi=100, bbox_inches='tight')
if len(sys.argv) == 1:
    plt.show()