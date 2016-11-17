#!/usr/bin/env python3

import sys
import os.path
import matplotlib
if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path
import csv

fig, ax = plt.subplots()

# read data

data = {}
with open("data/file_sizes.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        if not len(row) == 2:
            continue
        data[Path(row[1].split('/'))] = float(row[0])

# do the magic

hp = HierarchicalPie(data,
                     ax,
                     cmap=plt.get_cmap("hsv"),
                     plot_minimal_angle=0,
                     label_minimal_angle=1.5)

# Do not display values
hp.format_value_text = lambda value: None

# set plot attributes

hp.plot(setup_axes=True)
# noinspection PyProtectedMember
ax.set_title('Disk usage chart of this repository.\n'
             'Total size: {} bit'.format(int(hp._completed_pv[Path(("", ))])))
fig.set_size_inches(10, 10)

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')
if len(sys.argv) == 1 or "debug" not in sys.argv:
    plt.show()
