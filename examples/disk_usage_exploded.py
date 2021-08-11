#!/usr/bin/env python3

import os.path
from os.path import dirname, join, realpath
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, Path
import csv

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

file_size_data_file = realpath(join(dirname(__file__), "data", "file_sizes.txt"))
data = {}
with open(file_size_data_file) as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        if not len(row) == 2:
            continue
        data[Path(row[1].split("/"))] = float(row[0])


axs[0].set_title("Explosion scaled with (1/depth)^2")
axs[1].set_title("Uniform Explosion")
axs[2].set_title("Explode one slice")
axs[3].set_title("Explode wedges independently")

sbps = [
    SunburstPlot(
        data,
        ax,
        cmap=plt.get_cmap("hsv"),
        plot_minimal_angle=0,
        label_minimal_angle=1.5,
    )
    for ax in axs
]


def wedge_gap0(path: Path):
    return 0, 1 / (1 + len(path)) ** 2


# noinspection PyUnusedLocal
def wedge_gap1(path: Path):
    return 0, 0.1


def wedge_gap2(path: Path):
    if path == Path((".", ".git", "objects")):
        return 0, 0.2
    else:
        return 0, 0


def wedge_gap3(path: Path):
    if len(path) == 1:
        return 0.1, 0.1
    elif path == Path((".", ".git", "objects")):
        return 0, 0.1
    elif path == Path((".", ".git")):
        return 0, 0.3
    elif path.startswith(Path((".", ".git"))) and not path.startswith(
        Path((".", ".git", "objects"))
    ):
        return 0.075, 0.075
    else:
        return 0, 0


sbps[0].wedge_spacing = wedge_gap0
sbps[1].wedge_spacing = wedge_gap1
sbps[2].wedge_spacing = wedge_gap2
sbps[3].wedge_spacing = wedge_gap3


for i, sbp in enumerate(sbps):
    sbp.format_value_text = lambda path: ""
    sbp.format_path_text = lambda path: ""
    sbp.plot(setup_axes=True)


fig.tight_layout(pad=0.5)

# save/show plot

fig.savefig(
    os.path.join(
        os.path.dirname(__file__),
        "figures",
        "{}.png".format(os.path.basename(__file__)),
    ),
    dpi=100,
    bbox_inches="tight",
)

if __name__ == "__main__":
    plt.show()
