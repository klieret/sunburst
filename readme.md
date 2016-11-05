# Hierarchical Pie Plots for the python3 Pyplot library

Suppose you have an hierarchical graph like such

![graph](readme_files/example_numbering.png)

where each *vertex* is assigned a certain weight or number. 
This module plots this in a multi-level Pie plot:

![screenshot](readme_files/scrot.png)

with this module this can be done in but a few steps:

```python
#!/usr/bin/env python3

import example_paths
import matplotlib.pyplot as plt
from hpie import HierarchicalPie

fig, ax = plt.subplots()

# import the data & do the magic
pathvalues = example_paths.numbering_pv
hp = HierarchicalPie(pathvalues, ax)

# plot
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
