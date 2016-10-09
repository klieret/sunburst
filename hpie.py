#!/usr/bin/env python3

import example_paths
import collections
from typing import Dict, List
from path import Path
e_pathtimes = example_paths.pathtimes
from itertools import groupby
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np


def complete(pathvalues: Dict[Path, float]) -> Dict[Path, float]:
    """ Suppose we have a pathvalue dictionary of the form
    {1.1.1: 12.0} (only one entry). Complete will desect each path and
    assign its value to the truncated path: I.e. "", 1.1 and 1.1.1. Thus we
    would get {1: 12.0, 1.1: 12.0, 1.1.1: 12.0}. For more items the values will
    be summed accordingly.
    :param pathvalues: {path: value} dictionary
    :return: {path: value} dictionary
    """
    # fixme: highly problematic! What if "1" and "1.1" is given? Clarify!
    completed = collections.defaultdict(float)
    for path, value in pathvalues.items():
        # len(path) +1 ensures that also the whole tag is considered:
        for level in range(len(path) + 1):
            completed[path[:level]] += value
    return completed


def structurize(paths: List[Path]) -> List[List[List[Path]]]:
    """ Takes a list of paths and groups the paths first by length (empty
    path length 0)and then by the parent (path[:len(path) - 1]).
    Example:
    [
        [ [''] ],                    # level 0: empty path = root
        [ [1, 2, 3] ],               # level 1: only one group, because all
                                     #   elements share the same parent
        [ [1.1, 1.2], [3.1, 3.2] ],  # (in case 2 doesn't have any children)
        [ [1.1.1, 1.1.2], [1.2.1, 1.2.2], [3.1.1], [3.2.1] ]
    ]
    :param paths: Paths
    :return: [[Paths grouped by parents] grouped by levels.]
    """
    structured = []  # return value

    # we do this in two stepts via the iteritems.groupby function, first
    # using the level, then the parent function as keys.
    # (Note that sorting is nescessary before calling groupby!)

    def level(path):
        return len(path)

    def parent(path):
        return path.parent()

    paths.sort(key=level)
    paths_by_level = (list(group) for _, group in groupby(paths, key=level))
    for paths_of_level in paths_by_level:
        paths_of_level.sort(key=parent)
        paths_by_parent = [list(group) for _, group in
                           groupby(paths_of_level, key=parent)]
        structured.append(paths_by_parent)

    return structured


Angles = collections.namedtuple('Angles', ['theta1', 'theta2'])


def calculate_angles(structured_paths: List[List[List[Path]]],
                     path_values: Dict[Path, float]) -> Dict[Path, Angles]:
    angles = {}  # return value
    # the total sum of all elements (on one level)
    value_sum = path_values[Path(())]
    for level_no, groups in enumerate(structured_paths):
        for group in groups:
            for path_no, path in enumerate(group):
                # First we determine the starting angle  (theta1) for the wedge
                # corresponding to the path.
                if level_no == 0:
                    # This corresponds to the inner circle (because level 0
                    # only contains the empty path, the root of the whole tree)
                    theta1 = 0
                elif path_no == 0:
                    # The first path of a group. Since the wedges must be
                    # aligned with the parent, we have to get this value
                    # from the parent.
                    theta1 = angles[path.parent()].theta1
                else:
                    # we continue the wedge where the previous one had stopped
                    theta1 = theta2
                # Now we determine the ending angle based on the fraction of
                # the value.
                theta2 = theta1 + 360 * path_values[path]/value_sum
                angles[path] = Angles(theta1, theta2)
    return angles


class HierarchicalPie(object):
    def __init__(self, pathvalues):
        self.input_pv = pathvalues

        self.completed_pv = complete(self.input_pv)
        self.paths = list(self.completed_pv.keys())
        self.max_len = max((len(path) for path in self.paths))
        self.structured_paths = structurize(self.paths)
        self.angles = calculate_angles(self.structured_paths, self.completed_pv)

        self.cmap = plt.get_cmap('rainbow')
        self.edgecolor = "b"

        self.origin = (0, 0)
        self.ring_width = 0.4
        self.inner_circle_width = 0

        self.wedges = [self.wedge(path) for path in self.paths]

    def edge_color(self, path):
        return (0, 0, 0, 1)

    def edge_width(self, path):
        # todo: implement
        return 1

    def face_color(self, path):
        # take the middle angle, else the first wedge will have the same color
        # as its parent or at least make sure, that we don't get the value 0
        # (white or black in a lot of color maps)
        if len(path) == 0:
            color = (1, 1, 1, 1)
        else:
            angle = (self.angles[path].theta1 + self.angles[path].theta2) / 2

            color = list(self.cmap(angle/360))
            # make the color get lighter with progressing level
            color[3] = 1 - (len(path) - 1) / (self.max_len - 1)
        return tuple(color)

    def format_value(self, value):
        # fixme: overwrite with function from before
        hours = int(value/60)
        minutes = int(value - hours * 60)
        if hours:
            return "{}h{}".format(hours, minutes)
        else:
            return str(minutes)

    def path_text(self, path):
        return "{} ({})".format(path, self.format_value(self.completed_pv[path]))

    def radial_text(self, path):
        theta1, theta2 = self.angles[path].theta1, self.angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = (self.inner_circle_width + (1-0.5 + len(path)) * self.ring_width)
        mid_x = self.origin[0] + radius * np.cos(np.deg2rad(angle))
        mid_y = self.origin[1] + radius * np.sin(np.deg2rad(angle))

        if 0 <= angle < 90:
            rotation = angle
        elif 90 <= angle < 270:
            rotation = angle - 180
        elif 270 < angle <= 360:
            rotation = angle - 360
        else:
            raise ValueError

        plt.text(mid_x, mid_y, self.path_text(path), ha="center", va="center",
                 rotation=rotation)

    def tangential_text(self, path):
        theta1, theta2 = self.angles[path].theta1, self.angles[path].theta2
        angle = (theta1 + theta2) / 2
        print(angle)
        radius = (self.inner_circle_width + (1-0.5 + len(path)) * self.ring_width)
        mid_x = self.origin[0] + radius * np.cos(np.deg2rad(angle))
        mid_y = self.origin[1] + radius * np.sin(np.deg2rad(angle))

        if 0 <= angle < 90:
           rotation = angle - 90
        elif 90 <= angle < 180:
            rotation = angle - 90
        elif 180 <= angle < 270:
            rotation = angle - 270
        elif 270 <= angle < 360:
            rotation = angle - 270
        else:
            raise ValueError
        print(path, mid_x, mid_y, angle, rotation)
        plt.text(mid_x, mid_y, self.path_text(path), ha="center", va="center",
                 rotation=rotation)

    def plot(self, ax):
        for w in self.wedges:
            ax.add_patch(w)
        for path in self.paths:
            if len(path)*(self.angles[path].theta2 - self.angles[path].theta1) > 90:
                self.tangential_text(path)
            else:
                self.radial_text(path)

    def wedge(self, path):
        return Wedge((self.origin[0], self.origin[1]),
                     (len(path) +1) * self.ring_width,
                     self.angles[path].theta1,
                     self.angles[path].theta2,
                     width=self.ring_width,
                     label=self.path_text(path),
                     facecolor=self.face_color(path),
                     edgecolor=self.edge_color(path),
                     fill=True)


fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_ylim([-2, 2])
ax.set_xlim([-2, 2])

hp = HierarchicalPie(e_pathtimes)
hp.plot(ax)

plt.show()