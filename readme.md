# Hierarchical Pie Plots for the python3 Pyplot library

[![Build Status](https://travis-ci.org/klieret/pyplot-hierarchical-pie.svg?branch=master)](https://travis-ci.org/klieret/pyplot-hierarchical-pie)

![screenshot](https://cloud.githubusercontent.com/assets/13602468/20237536/68419834-a8d5-11e6-9e43-bc33a645c411.png)

with this module such figures can be done in but a few steps.

## Installation

As this project is still in development, you have to first have to clone the repository before running ```pip```:

```sh
git clone https://github.com/klieret/pyplot-hierarchical-pie
cd pyplot-hierarchical-pie
sudo pip3 install .
```

## Minimal example

A minimal example:
([https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/example_hpie.py](```example_hpie.py```)):

```python
#!/usr/bin/env python3

import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path
import random

fig, ax = plt.subplots()

# set up some data

paths = [Path(tuple(a)) for a in "1 2 12 13 111 112 113 121 122 211 221 222 "
                                 "1111 1112 1121".split(" ")]
pathvalues = {path: random.uniform(1, 100) for path in paths}

# do the magic

hp = HierarchicalPie(pathvalues, ax)

# set plot attributes

hp.plot()
ax.autoscale()
ax.set_aspect("equal")
ax.autoscale_view(True, True, True)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.margins(x=0.1, y=0.1)
ax.set_title('Example HPie')

plt.show()
```

Other examples are in ```examples```. 