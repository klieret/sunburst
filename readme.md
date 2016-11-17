[![Build Status](https://travis-ci.org/klieret/pyplot-hierarchical-pie.svg?branch=master)](https://travis-ci.org/klieret/pyplot-hierarchical-pie)


# Hierarchical Pie Charts for the python3 Pyplot library

```HPie``` is a module to create "Ring charts" or "Hierarchical Pie Charts" (also called "Multilevel Pie Charts" or "Sunburst Charts" ) together with the [```matplotlib```](http://matplotlib.org/) package. 
Quoting [wikipedia](https://en.wikipedia.org/wiki/Pie_chart#Ring_chart_.2F_Sunburst_chart_.2F_Multilevel_pie_chart):


> A ring chart, also known as a sunburst chart or a multilevel pie chart, is used to visualize hierarchical data, depicted by concentric circles. The circle in the centre represents the root node, with the hierarchy moving outward from the center. A segment of the inner circle bears a hierarchical relationship to those segments of the outer circle which lie within the angular sweep of the parent segment.

A prominent example are disk usage charts (see [```examples/disk_usage_plot.py```](examples/disk_usage_plot.py) for this example):

![screenshot](https://cloud.githubusercontent.com/assets/13602468/20408444/c8cb6a56-ad15-11e6-8f5c-1abef69dc551.png)



## Installation

As this project is still in development, you have to first have to clone the repository before running [```pip3```](https://pip.pypa.io/en/stable/):

```sh
git clone https://github.com/klieret/pyplot-hierarchical-pie
cd pyplot-hierarchical-pie
sudo pip3 install .
```

If you want to check if everything will work properly on your system, you can run:

```sh
python3 -m unittest discover
```

All of the examples from the toplevel of [```examples/```](examples/) will be run as well, so you can check [```examples/figures```](examples/figures) for the rendered graphics.

To uninstall, run

```sh
sudo pip3 uninstall hpie
```

To check if this package is installed, run

```sh
pip3 freeze | grep hpie
```


## Minimal example

You can find several examples at [```examples/```](examples/). The most basic example is [```minimal_example_hpie.py```](examples/minimal_example_hpie.py):

```python
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, stringvalues_to_pathvalues

fig, ax = plt.subplots()

# set up some random data

data = stringvalues_to_pathvalues({
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

hp = HierarchicalPie(data, ax)

# set plot attributes

hp.plot(setup_axes=True)
ax.set_title('Example HPie')

# save/show plot

plt.show()

```

Running this script with ```python3 minimal_example_hpie.py``` will produce the following plot:

![screenshot_minmal_example](https://cloud.githubusercontent.com/assets/13602468/20408443/c8c8c1d4-ad15-11e6-86a6-868dc98e91d0.png)

### The Data 

Note that the value corresponding to path is always the value *excluding* the values of the children of the path. Therefore plotting the ```HierarchicalPie``` object computes a "completed" version of the "pathvalue dictionary". You can check this with the ```HierarchicalPie._completed_pv``` instance variable which gets initialized after calling ```HierarchicalPie.plot(*args)```. Running our minimal example prints the following:

```python
hp._completed_pv.items() = {
	Path((, )): 442.2,  # = the total sum of all items = 
	                    # = 36.12 + 44.32 + 37.15 + 23.98 + ...
	Path(('ipsum', )): 164.19000000000003,  # = sum of "ipsum" and all of its children = 
	                                        # = 40.45 + 29.34 + 94.4
	Path(('ipsum', 'eirmod', )): 123.74000000000001, # = sum of ipsum/eirmod and all of its children =
	                                                 # = 29.34 + 94.4
	Path(('ipsum', 'eirmod', 'dolor', )): 94.4,
	Path(('lorem', )): 278.01,
	Path(('lorem', 'eirmod', )): 56.769999999999996,
	Path(('lorem', 'eirmod', 'lorem', )): 45.65,
	Path(('lorem', 'sadipscing', )): 185.12,
	Path(('lorem', 'sadipscing', 'dolor', )): 44.32,
	Path(('lorem', 'sadipscing', 'lorem', )): 37.15,
	Path(('lorem', 'sadipscing', 'nonumy', )): 23.98,
}

```

[```test_hpie.py```](hpie/tests/test_calc.py) contains a test which explicitly checks that this is working correctly.

### Ring Charts

Thus you get ring charts, if and only if all of the non-zero values correspond to paths with the same length. E.g. if we change the above data as follows (by lengthening the paths with question marks and removing the entry for the empty path):

```python
data = stringvalues_to_pathvalues({
    'ipsum/?/?':                 40.45,
    'ipsum/eirmod/?':            29.34,
    'ipsum/eirmod/dolor':        94.4,
    'lorem/?/?':                 36.12,
    'lorem/sadipscing/dolor':    44.32,
    'lorem/sadipscing/lorem':    37.15,
    'lorem/sadipscing/nonumy':   23.98,
    'lorem/eirmod/?':            11.12,
    'lorem/eirmod/lorem':        45.65,
    'lorem/sadipscing/?':        79.67,
})
```

we should get a classical ring chart. This is [```minimal_example_rings.py```](examples/minimal_example_hpie.py). Running it via ```python3 minimal_example_hpie.py``` yields the following plot, which indeed just fills up the white space of the above plot with wedges labeled ```?```.

![screenshot minimal_example rings](https://cloud.githubusercontent.com/assets/13602468/20408445/c8cdf4ec-ad15-11e6-9a10-2758c3469f9d.png)