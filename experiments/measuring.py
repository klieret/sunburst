""" Shows that measuring text before and after drawing is the same as long
as you have the correct renderer."""

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

import matplotlib.transforms as mtransforms
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect("equal")
ax.plot(range(10))
strings = ['really, really, really', 'long', 'labels']
texts = [plt.text(1, i+1, string) for i, string in enumerate(strings)]

for i, text in enumerate(texts):
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)
    transform = ax.transData.inverted().transform
    width, height = (transform([bbox.width, bbox.height]) - transform([0,0]))
    print("{0}: {1:.2f}x{2:.2f}".format(text.get_text(), width, height))
    plt.plot([1, 1+width], [i+1, i+1])
    ax.add_patch(Wedge((5, i+1), 5, 0, 360, width=width))

plt.show()
