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

To uninstall, run

```sh
sudo pip3 uninstall hpie
```

To check if this package is installed, run

```sh
pip3 freeze | grep hpie
```


## Minimal example

(Even more minimal) version of [```minimal_example_hpie.py```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_hpie.py):

```python
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path

fig, ax = plt.subplots()

# set up some random data

data = {
    Path(('lorem', )): 36,
    Path(('ipsum', 'eirmod', 'dolor')): 94,
    Path(('lorem', 'sadipscing', 'dolor')): 44,
    Path(('lorem', 'sadipscing', 'lorem')): 37,
    Path(('lorem', 'eirmod', 'lorem')): 45,
    Path(('ipsum', 'eirmod')): 29,
    Path(('lorem', 'eirmod')): 11,
    Path(('lorem', 'sadipscing', 'nonumy')): 23,
    Path(('ipsum',)): 40,
    Path(('lorem', 'sadipscing')): 79,
}

# do the magic

hp = HierarchicalPie(data, ax)

# set plot attributes

hp.plot(setup_axes=True)
ax.set_title('Example HPie')

# save/show plot

plt.show()

```

Running this script with ```python3 minimal_example_hpie.py``` will produce the following plot:

![screenshot_minmal_example](https://cloud.githubusercontent.com/assets/13602468/20247642/559798a8-a9d1-11e6-931c-bcf0869c8198.png)

Other examples are in [```examples```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/).  