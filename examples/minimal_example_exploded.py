#!/usr/bin/env python3

import sys
import os.path
import matplotlib
if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

data = {
    Path(('ipsum',)):                           40.45,  # note the ','
    Path(('ipsum', 'eirmod')):                  29.34,
    Path(('ipsum', 'eirmod', 'dolor')):         94.4,
    Path(('lorem', )):                          36.12,
    Path(('lorem', 'sadipscing', 'dolor')):     44.32,
    Path(('lorem', 'sadipscing', 'lorem')):     37.15,
    Path(('lorem', 'sadipscing', 'nonumy')):    23.98,
    Path(('lorem', 'eirmod')):                  11.12,
    Path(('lorem', 'eirmod', 'lorem')):         45.65,
    Path(('lorem', 'sadipscing')):              79.67,
}


axs[0].set_title('Standard HPie')
axs[1].set_title('Completely exploded')
axs[2].set_title('Explode one slice')
axs[3].set_title('Explode multiple slices')

hps = [HierarchicalPie(data, ax) for ax in axs]

# noinspection PyUnusedLocal
def wedge_gap1(path: Path):
    return 0, 0.1


def wedge_gap2(path: Path):
    if path == Path(("ipsum", )):
        return 0, 0.2
    else:
        return 0, 0


def wedge_gap3(path: Path):
    if path == Path(("lorem", "eirmod")):
        return 0, 0.35
    elif path == Path(("ipsum", )):
        return 0, 0.5
    elif path.startswith(Path(("lorem", ))):
        return 0, 0.1
    else:
        return 0, 0

hps[1].wedge_gap = wedge_gap1
hps[2].wedge_gap = wedge_gap2
hps[3].wedge_gap = wedge_gap3


for i, hp in enumerate(hps):
    hp.format_value_text = lambda path: ""
    hp.plot(setup_axes=True)


fig.tight_layout(pad=0.5)

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')
if len(sys.argv) == 1 or "debug" not in sys.argv:
    plt.show()
