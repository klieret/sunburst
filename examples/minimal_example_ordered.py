#!/usr/bin/env python3

import os.path
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, charlist_to_ordered_pv, charvalues_to_pv

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

data = charvalues_to_pv(
    {
        "1": 5.0,
        "111": 92.0,
        "1111": 15.0,
        "1112": 99.0,
        "112": 0.0,
        "1121": 70.0,
        "113": 27.0,
        "12": 51.0,
        "121": 43.0,
        "122": 29.0,
        "13": 69.0,
        "2": 29.0,
        "211": 43.0,
    }
)

data_ordered = charlist_to_ordered_pv(
    [
        "2",
        29.0,
        "1",
        5.0,
        "111",
        92.0,
        "1112",
        99.0,
        "1111",
        15.0,
        "112",
        0.0,
        "1121",
        70.0,
        "113",
        27.0,
        "12",
        51.0,
        "122",
        29.0,
        "121",
        43.0,
        "13",
        69.0,
        "211",
        43.0,
    ]
)


axs[0].set_title("Default Order")
axs[1].set_title("Alphabetic Order")
axs[2].set_title("Order by Value Increasing")
axs[3].set_title("Keep Order")

sbps = [
    SunburstPlot(data, axs[0]),
    SunburstPlot(data, axs[1], order="key"),
    SunburstPlot(data, axs[2], order="value reverse"),
    SunburstPlot(data_ordered, axs[3], order="keep"),
]

for i, sbp in enumerate(sbps):
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
