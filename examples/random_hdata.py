#!/usr/bin/env python3

# fixme: needs some clean up and fixing

from random import randrange as rr
from typing import List
import sys
import os.path
import matplotlib

if "debug" in sys.argv[1:]:
    matplotlib.use("AGG")
import matplotlib.pyplot as plt
from sunburst import SunburstPlot, Path


class RandomHdata(object):
    def __init__(self, loremipsum, population_numbers: List[int]):
        self.population_numbers = population_numbers

        self.loremipsum = loremipsum

        self.level_population = [
            self.random_items(pn) for pn in population_numbers
        ]

    def random_items(self, n):
        """Generates n random items from self.loremipsum."""
        return [self.loremipsum[rr(0, len(self.loremipsum))] for _ in range(n)]

    def random_path(self, length):
        path = Path(
            [
                self.level_population[level][
                    rr(0, self.population_numbers[level])
                ]
                for level in range(length)
            ]
        )
        return path

    def paths(self, num_paths):
        return sorted(
            [
                self.random_path(rr(1, len(self.population_numbers) + 1))
                for _ in range(num_paths)
            ],
            key=lambda p: str(p),
        )


if __name__ == "__main__":
    import sys

    if not len(sys.argv) == 4:
        print("Wrong syntax")
        sys.exit(1)
    if sys.argv[1] == "lorem":
        loremipsum = (
            "Lorem ipsum dolor ame consetetur sadipscing elit "
            "sed diam nonumy eirmod tempor invidunt "
            "labore dolore".split(" ")
        )
    else:
        loremipsum = list(map(str, range(10)))
    p_numbers = [int(i) for i in sys.argv[2].split(",")]
    n_paths = int(sys.argv[3])
    rhd = RandomHdata(loremipsum, p_numbers)
    paths = rhd.paths(n_paths)
    pathvalues = {path: rr(1, 1000) / 10 for path in paths}

    # pretty print
    # print(data)
    print("{")
    for path, value in pathvalues.items():
        print("\t{}: {},".format(repr(path), value))
    print("}")

    fig, ax = plt.subplots()

    sbp = SunburstPlot(pathvalues, ax)

    sbp.plot(setup_axes=True)
    ax.set_title("Example SunburstPlot")

    # save/show plot

    fig.savefig(
        os.path.join(
            os.path.dirname(__file__),
            "figures",
            "{}.png".format(os.path.basename(__file__)),
        ),
        dpi=100,
        bbox_inches="tight",
    )
