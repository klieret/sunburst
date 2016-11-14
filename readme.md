[![Build Status](https://travis-ci.org/klieret/pyplot-hierarchical-pie.svg?branch=master)](https://travis-ci.org/klieret/pyplot-hierarchical-pie)


# Hierarchical Pie Plots for the python3 Pyplot library

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

There are several examples in the directory [```examples```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/).  

A (even more minimal) version of [```minimal_example_hpie.py```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_hpie.py):

```python
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path

fig, ax = plt.subplots()

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

### The Data 

Note that the value corresponding to path is always the value *excluding* the values of the children of the path. Therefore plotting the ```HierarchicalPie``` object computes a "completed" version of the "pathvalue dictionary". You can check this with the ```HierarchicalPie._completed_pv``` instance variable which gets initialized after calling ```HierarchicalPie.plot(*args)```. For example ```python3 minimal_example_hpie.py``` will output:

In the above example:

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

[```test_hpie.py```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/hpie/tests/test_hpie.py) contains a test which explicitly checks that this is working correctly.

### Ring Charts

Thus you get ring charts, if and only if all of the non-zero values correspond to paths with the same length. E.g. if we change the above data as follows (by lengthening the paths with question marks):

```python
data = {
    Path(('ipsum', 'eirmod', 'dolor')):         94.4,
    Path(('lorem', 'sadipscing', 'dolor')):     44.32,
    Path(('lorem', 'sadipscing', 'lorem')):     37.15,
    Path(('lorem', 'sadipscing', 'nonumy')):    23.98,
    Path(('lorem', 'eirmod', 'lorem')):         45.65,
}
```

we should get a classical ring chart. This is [```minimal_example_rings.py```](https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_hpie.py). Running it via ```python3 minimal_example_hpie.py``` yields the following plot, which indeed just fills up the white space of the above plot with wedges labeled ```?```.

![screenshot minimal_example rings](https://cloud.githubusercontent.com/assets/13602468/20247923/619b7662-a9d9-11e6-9d87-ea5e3da60503.png)

## Caveats regarding initialization of Path objects

```Path``` objects must be initialized by a (possibly empty) iterable (but not a string) with (non-empty) strings as elements. Note that therefore the following lines of code will all fail:

```python
from hpie import Path

Path("test")        # initialization with a string
Path(("test"))      # ("test") gets simplified to "test". Correct: ("test", )
Path(("", "test"))  # empty string
Path("")            # empty string. If you want an empty path, use Path(())
Path()              # missing argument. If you want an empty path, use Path(())
```