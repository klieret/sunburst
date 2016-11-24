#!/usr/bin/env python3

import sys
import os.path
import matplotlib
import matplotlib.pyplot as plt
from hpie import HPie, stringvalues_to_pv

fig, ax = plt.subplots()

fig.set_size_inches(5, 5)

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

# do the magic

hp = HPie(data, ax, default_line_width=1)

# set plot attributes

def nothing(*args, **kwargs):
    return ""

hp.text = nothing


hp.plot(setup_axes=True)
# ax.set_title('Minimal Example')

# save/show plot

fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                         "{}.png".format(os.path.basename(__file__))),
            dpi=100,
            bbox_inches='tight')


if __name__ == "__main__":
    plt.show()

    # For the interpretation:
    print("hp._completed_pv.items() = {")
    # noinspection PyProtectedMember
    for path, value in sorted(hp._completed_pv.items(), key=lambda x: str(x[0])):
            print("\t{}: {},".format(repr(path), value))
    print("}")
