# Hierarchical Pie Plots for the python3 Pyplot library

Suppose you have an hierarchical graph like such

![graph](readme_files/example_numbering.png)

where each *vertex* is assigned a certain weight or number. 
This module plots this in a multi-level Pie plot:

![screenshot](readme_files/scrot.png)

with this module this can be done in but a few steps 
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
