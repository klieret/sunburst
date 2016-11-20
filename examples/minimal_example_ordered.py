#!/usr/bin/env python3

import os.path
import matplotlib
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path, stringvalues_to_pv

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

data = stringvalues_to_pv({
    'ipsum':                      40.45,
    'ipsum/eirmod':               29.34,
    'ipsum/eirmod/dolor':         94.4,
    'lorem':                      36.12,
    'lorem/sadipscing/dolor':     44.32,
    'lorem/sadipscing/lorem':     37.15,
    'lorem/sadipscing/nonumy':    23.98,
    'lorem/eirmod':               11.12,
    'lorem/eirmod/lorem':         45.65,
    'lorem/sadipscing':           79.67,
})


axs[0].set_title('Keeping Order')
axs[1].set_title('Alphabetic Order')
axs[2].set_title('Order by Value')
axs[3].set_title('Reverse Order by Value')

hps = [HierarchicalPie(data, axs[0], order="keep"),
       HierarchicalPie(data, axs[1], order="key"),
       HierarchicalPie(data, axs[2], order="value"),
       HierarchicalPie(data, axs[3], order="value reverse"),
       ]

for i, hp in enumerate(hps):
    print("******************************************************************")
    hp.plot(setup_axes=True)

fig.tight_layout(pad=0.5)

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')

if __name__ == "__main__":
    plt.show()
