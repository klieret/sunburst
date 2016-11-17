#!/usr/bin/env python3

from random import randrange as rr
from typing import List
import sys
import os.path
import matplotlib
if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from hpie import HierarchicalPie, Path


class RandomHdata(object):
    def __init__(self, population_numbers: List[int]):
        self.population_numbers = population_numbers

        self.loremipsum = "Lorem ipsum dolor ame consetetur sadipscing elit " \
                          "sed diam nonumy eirmod tempor invidunt " \
                          "labore dolore".split(" ")

        self.level_population = [self.random_items(pn) for pn
                                 in population_numbers]

    def random_items(self, n):
        """ Generates n random items from self.loremipsum.
        """
        return [self.loremipsum[rr(0, len(self.loremipsum))] for _ in range(n)]

    def random_path(self, length):
        path = Path([self.level_population[level][rr(0, self.population_numbers[level])] for level in range(length)])
        return path

    def paths(self, num_paths):
        return [self.random_path(rr(1, len(self.population_numbers) + 1)) for _ in range(num_paths)]

if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 3:
        print("Wrong syntax, goodbye.")
        # fixme
        sys.exit(0)
    p_numbers = [int(i) for i in sys.argv[1].split(',')]
    n_paths = int(sys.argv[2])
    rhd = RandomHdata(p_numbers)
    paths = rhd.paths(n_paths)
    pathvalues = {path: rr(1, 100) for path in paths}

    # pretty print
    # print(data)
    print("{")
    for path, value in pathvalues.items():
        print("\t{}: {},".format(repr(path), value))
    print("}")

    fig, ax = plt.subplots()

    hp = HierarchicalPie(pathvalues, ax)

    hp.plot(setup_axes=True)
    ax.set_title('Example HPie')

    # save/show plot

    fig.savefig(os.path.join(os.path.dirname(__file__), "figures",
                             "{}.png".format(os.path.basename(__file__))),
                dpi=100,
                bbox_inches='tight')