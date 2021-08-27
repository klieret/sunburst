#!/usr/bin/env python3

import pathlib
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, Path
import csv
import os

# read data

file_size_data_file = (
    pathlib.Path(__file__).resolve().parent / "data" / "file_sizes.txt"
)

fig, ax = plt.subplots()


data = {}
with open(file_size_data_file) as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        if not len(row) == 2:
            continue
        data[Path(row[1].split("/"))] = float(row[0])

# do the magic

sbp = SunburstPlot(
    data,
    ax,
    cmap=plt.get_cmap("hsv"),
    plot_minimal_angle=0,
    label_minimal_angle=1.5,
)

# Do not display values
sbp.format_value_text = lambda value: ""  # type: ignore

sbp.plot(setup_axes=True)

# set plot attributes
ax.set_title("Disk Usage Chart")

# save/show plot

fig.set_size_inches(10, 10)
fig.savefig(
    pathlib.Path(__file__).resolve().parent / "figures" / "disk_usage_plot.png",
    dpi=100,
    bbox_inches="tight",
)

if "NOPLOT" not in os.environ:
    plt.show()
