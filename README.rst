Hierarchical Pie Charts |Build Status| |Doc Status|
===================================================

✨ **This package is currently being reworked. Checkout the `sunburst` branch** ✨

\| `Introduction <#introduction>`__ \| `Features <#features>`__ \|
`Installation <#installation>`__ \| `Minimal
Example <#minimal-example>`__ \| `License <#license>`__ \|

.. |Build Status| image:: https://travis-ci.org/klieret/pyplot-hierarchical-pie.svg?branch=master
   :target: https://travis-ci.org/klieret/pyplot-hierarchical-pie

.. |Doc Status| image:: https://readthedocs.org/projects/pyplot-hierarchical-pie/badge/?version=latest
   :target: http://pyplot-hierarchical-pie.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**Check out the full documentation at** |readthedocs.io|_.

.. |readthedocs.io| replace:: **readthedocs.io**
.. _readthedocs.io: http://pyplot-hierarchical-pie.readthedocs.io/en/latest/

.. start-body

Introduction
------------

.. start-introduction

``sunburst`` is a module to create "Ring charts" or "Hierarchical Pie
Charts" (also called "Multilevel Pie Charts" or "Sunburst Charts")
together with the |matplotlib|_ package.
Quoting Wikipedia_:

    A ring chart, also known as a sunburst chart or a multilevel pie
    chart, is used to visualize hierarchical data, depicted by
    concentric circles. The circle in the centre represents the root
    node, with the hierarchy moving outward from the center. A segment
    of the inner circle bears a hierarchical relationship to those
    segments of the outer circle which lie within the angular sweep of
    the parent segment.

A prominent example are disk usage charts (see |du_example|_ for this example):

.. figure:: https://cloud.githubusercontent.com/assets/13602468/20408444/c8cb6a56-ad15-11e6-8f5c-1abef69dc551.png
   :alt: Hpie Example: Disk Usage Chart
   :align: center

.. |matplotlib| replace:: ``matplotlib``
.. _matplotlib: http://matplotlib.org/

.. _wikipedia: https://en.wikipedia.org/wiki/Pie_chart#Ring_chart_.2F_Sunburst_chart_.2F_Multilevel_pie_chart

.. |du_example| replace:: ``examples/disk_usage_plot.py``
.. _du_example: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/disk_usage_plot.py

Features
--------

``sunburst`` tries to be

-  Intuitive & Easy to use: After setting up your data and
   ``matplotlib``, not more than two lines are necessary to generate
   first plots (`minimal example`_).
-  Flexible & Robust: Wherever it makes sense, the methods of the
   ``SunburstPlot`` class are intended to be overwritten. Methods
   that are responsible for spacing, coloring, styling etc. of the
   ``wedges`` take the corresponding data point (``path``) as an
   argument, allowing to set most properties independently for each
   ``wedge``.

More specifically:

-  Clever positioning of labels, which - depending on space constraints
   are positioned in a tangentially or radially.
-  An easy way to "explode" the plot by redefining
   ``sunburst.wedge_spacing``
   (`example <https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_exploded.py>`__,
   `example <https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/disk_usage_exploded.py>`__).

.. _minimal example: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_sunburst.py


✨ Migration notice ✨
----------------------

For the first release to pypi, this package has been rebranded as ``sunburst``.
This includes non-backwards compatible changes to the API: Most importantly,
the ``HPie`` class is now ``SunburstPlot`` and many other changes.

To get the old version back, check out the ``old-hpie`` branch.

Installation
------------

As this project is still in development, you have to first have to clone
the repository before installing the package with
|pip3|_:

.. |pip3| replace:: ``pip3``
.. _pip3: https://pip.pypa.io/en/stable/

.. code:: sh

    git clone https://github.com/klieret/pyplot-hierarchical-pie

Alternatively click
`here <https://github.com/klieret/pyplot-hierarchical-pie/archive/master.zip>`__
to download the current state of the master branch. Change to the
downloaded directory. To check that everything will work properly on
your system, run:

.. code:: sh

    python3 -m unittest discover

To install, run

.. code:: sh

    sudo pip3 install .

All of the examples from the toplevel of |examples|_
will be run as well, so you can check
|figures|_ for the rendered graphics.

.. |examples| replace:: ``examples/``
.. |figures| replace:: ``examples/figures``
.. _examples: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/
.. _figures: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/figures/

To uninstall, run

.. code:: sh

    sudo pip3 uninstall sunburst

To check if this package is installed, run

.. code:: sh

    pip3 freeze | grep sunburst

Minimal example
---------------

You can find several examples at |examples|_. Remember
to either install this package or update your ``PYTHONPATH`` via (linux)

.. code:: sh

    source setup_path.py

before running the examples. The most basic example is |minimal|:

.. |minimal| replace:: minimal_example_sunburst.py
.. _minimal: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_sunburst.py

.. code:: python

    import matplotlib.pyplot as plt
    from sunburst import SunburstPlot, stringvalues_to_pv

    fig, ax = plt.subplots()

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

    sbp = SunburstPlot(data, ax)

    # set plot attributes

    sbp.plot(setup_axes=True)
    ax.set_title('Example SunburstPlot')

    # save/show plot

    plt.show()

Running this script with ``python3 minimal_example_sunburst.py`` will
produce the following plot:

.. figure:: https://cloud.githubusercontent.com/assets/13602468/20408443/c8c8c1d4-ad15-11e6-86a6-868dc98e91d0.png
   :alt: Screenshot Minimal Example
   :align: center


The Data
~~~~~~~~

Note that the value corresponding to path is always the value
*excluding* the values of the children of the path. Therefore plotting
the ``SunburstPlot`` object computes a "completed" version of the
"pathvalue dictionary". You can check this with the
``SunburstPlot._completed_pv`` instance variable which gets
initialized after calling ``SunburstPlot.plot(*args)``. Running our
minimal example prints the following:

.. code:: python

    sbp._completed_pv.items() = {
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

|test_calc|_ contains an
explicit test of this calculation based on a similar example.

.. |test_calc| replace:: ``sunburst/tests/test_calc.py``
.. _test_calc: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/sunburst/tests/test_calc.py

Ring Charts
~~~~~~~~~~~

Thus you get ring charts, if and only if all of the non-zero values
correspond to paths with the same length. E.g. if we change the above
data as follows (by lengthening the paths with question marks and
removing the entry for the empty path):

.. code:: python

    data = stringvalues_to_pv({
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

we should get a classical ring chart. This is
|rings|_ .
Running it via ``python3 minimal_example_rings.py`` yields the following
plot, which indeed just fills up the white space of the above plot with
wedges labeled ``?``.

.. |rings| replace:: ``minimal_example_rings.py``
.. _rings: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/examples/minimal_example_rings.py

.. figure:: https://cloud.githubusercontent.com/assets/13602468/20408445/c8cdf4ec-ad15-11e6-9a10-2758c3469f9d.png
   :alt: Minimal Example Rings
   :align: center

.. start-license

License
-------

This project is licensed under the *BSD 3-Clause License*, see |license|_.

.. |license| replace:: ``LICENSE.txt``
.. _license: https://github.com/klieret/pyplot-hierarchical-pie/blob/master/LICENSE.txt
