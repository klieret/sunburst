#!/usr/bin/env python3

import pathlib
import os
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, stringvalues_to_pv

fig, ax = plt.subplots()

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

# do the magic

sbp = SunburstPlot(data, ax)

# set plot attributes

sbp.plot(setup_axes=True)
ax.set_title("Minimal Example")

# save/show plot

fig.savefig(
    pathlib.Path(__file__).resolve().parent
    / "figures"
    / "minimal_example_sunburst.png",
    dpi=100,
    bbox_inches="tight",
)

if "NOPLOT" not in os.environ:
    plt.show()

# For the interpretation:
print("sbp._completed_pv.items() = {")
# noinspection PyProtectedMember
for path, value in sorted(sbp._completed_pv.items(), key=lambda x: str(x[0])):
    print("\t{}: {},".format(repr(path), value))
print("}")
