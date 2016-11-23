#!/usr/bin/env python3

import os.path
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, charlist_to_ordered_pv, charvalues_to_pv

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

axs = [ax0, ax1, ax2, ax3]

fig.set_size_inches(10, 10)

# set up some random data

data = charvalues_to_pv({'1': 5.,
                         '111': 92.,
                         '1111': 15.,
                         '1112': 99.,
                         '112': 0.,
                         '1121': 70.,
                         '113': 27.,
                         '12': 51.,
                         '121': 43.,
                         '122': 29.,
                         '13': 69.,
                         '2': 29.,
                         '211': 43.})

data_ordered = charlist_to_ordered_pv([
                           '2', 29.,
                           '1', 5.,
                           '111', 92.,
                           '1112', 99.,
                           '1111', 15.,
                           '112', 0.,
                           '1121', 70.,
                           '113', 27.,
                           '12', 51.,
                           '122', 29.,
                           '121', 43.,
                           '13', 69.,
                           '211', 43.,
])


axs[0].set_title('Default Order')
axs[1].set_title('Alphabetic Order')
axs[2].set_title('Order by Value Increasing')
axs[3].set_title('Keep Order')

hps = [HierarchicalPie(data, axs[0]),
       HierarchicalPie(data, axs[1], order="key"),
       HierarchicalPie(data, axs[2], order="value"),
       HierarchicalPie(data_ordered, axs[3], order="keep")]

for i, hp in enumerate(hps):
    hp.plot(setup_axes=True)

fig.tight_layout(pad=0.5)

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')

if __name__ == "__main__":
    plt.show()
