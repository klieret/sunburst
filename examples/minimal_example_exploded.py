#!/usr/bin/env python3

import os.path
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, Path, stringvalues_to_pv

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

data = stringvalues_to_pv(
    {
        "ipsum": 40.45,
        "ipsum/eirmod": 29.34,
        "ipsum/eirmod/dolor": 94.4,
        "lorem": 36.12,
        "lorem/sadipscing/dolor": 44.32,
        "lorem/sadipscing/lorem": 37.15,
        "lorem/sadipscing/nonumy": 23.98,
        "lorem/eirmod": 11.12,
        "lorem/eirmod/lorem": 45.65,
        "lorem/sadipscing": 79.67,
    }
)


axs[0].set_title("Standard SunburstPlot")
axs[1].set_title("Completely exploded")
axs[2].set_title("Explode one slice")
axs[3].set_title("Explode multiple slices")

sbps = [SunburstPlot(data, ax) for ax in axs]


# noinspection PyUnusedLocal
def wedge_gap1(path: Path):
    return 0, 0.1


def wedge_gap2(path: Path):
    if path == Path(("ipsum",)):
        return 0, 0.2
    else:
        return 0, 0


def wedge_gap3(path: Path):
    if path == Path(("lorem", "eirmod")):
        return 0, 0.35
    elif path == Path(("ipsum",)):
        return 0, 0.5
    elif path.startswith(Path(("lorem",))):
        return 0, 0.1
    else:
        return 0, 0


sbps[1].wedge_spacing = wedge_gap1
sbps[2].wedge_spacing = wedge_gap2
sbps[3].wedge_spacing = wedge_gap3


for i, sbp in enumerate(sbps):
    sbp.format_value_text = lambda path: ""
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
