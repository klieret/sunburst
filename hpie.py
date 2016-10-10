#!/usr/bin/env python3

import collections
from typing import Dict, List
from path import Path
from itertools import groupby
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np


# future: sorting & unsorting


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
            theta2 = None  # else pycharm complains about theta2 undefined
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
    def __init__(self,
                 pathvalues,
                 axes,
                 origin=(0, 0),
                 cmap=plt.get_cmap('autumn'),
                 default_ring_width=0.4,
                 default_edge_color=(0, 0, 0, 1),
                 default_edge_width=1):

        # *** Input & Config *** (emph)
        self.input_pv = pathvalues
        self.axes = axes
        self.cmap = cmap
        self.origin = origin
        self.default_ring_width = default_ring_width
        self.default_edge_color = default_edge_color
        self.default_edge_width = default_edge_width

        # *** Variables used for computation *** (emph)
        self._completed_pv = None        # type: Dict[Path, float]
        self._paths = None               # type: List[Path]
        self._max_level = None           # type: int
        self._structured_paths = None    # type: List[List[List[Path]]]
        self._angles = None              # type: Dict[Path, Angles]

        # *** "Output" *** (emph)
        self.wedges = None               # type: Dict[Path, Wedge]

    def prepare_data(self):
        self._completed_pv = complete(self.input_pv)
        self._paths = list(self._completed_pv.keys())
        self._max_level = max((len(path) for path in self._paths))
        self._structured_paths = structurize(self._paths)
        self._angles = calculate_angles(self._structured_paths,
                                        self._completed_pv)
        self.wedges = [self.wedge(path) for path in self._paths]

    def _is_outmost(self, path):
        # is there a descendant of path?
        # to speed up things we use self._structured_paths
        level = len(path)
        if level == self._max_level:
            return True
        for group in self._structured_paths[level + 1]:
            for p in group:
                if p.startswith(path):
                    return False
                # all paths in this group start the same
                continue
        return True


    def wedge_width(self, level):
        if level == 0:
            return 0.75 * self.default_ring_width
        else:
            return 0.4

    def _wedge_outer_radius(self, level):
        # todo: make dependent of path to allow to explode slices
        return sum(self.wedge_width(level) for level in range(level + 1))

    def _wedge_inner_radius(self, level):
        # todo: make dependent of path to allow to explode slices
        return sum(self.wedge_width(level) for level in range(level))

    def _wedge_mid_radius(self, level):
        return (self._wedge_outer_radius(level) +
                self._wedge_inner_radius(level)) / 2

    def edge_color(self, path):
        return self.default_edge_color

    def edge_width(self, path):
        # todo: implement
        return self.default_edge_width

    def face_color(self, path):
        # take the middle angle, else the first wedge will have the same color
        # as its parent or at least make sure, that we don't get the value 0
        # (white or black in a lot of color maps)
        if len(path) == 0:
            color = (1, 1, 1, 1)
        else:
            angle = (self._angles[path].theta1 + self._angles[path].theta2) / 2
            color = list(self.cmap(angle/360))
            # make the color get lighter with increasing level
            color[3] = 1 - (len(path) - 1) / (self._max_level + 1)
        return tuple(color)

    def format_value(self, value):
        # fixme: overwrite with function from before
        hours = int(value/60)
        minutes = int(value - hours * 60)
        if hours:
            return "({}h{})".format(hours, minutes)
        else:
            return "({})".format(minutes)

    def path_text(self, path):
        return path[-1] if path else ""

    def _radial_text(self, path):
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        level = len(path)
        radius = self._wedge_mid_radius(level)
        if self._is_outmost(path):
            radius = self._wedge_inner_radius(level)

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

        # If the wedge is on the outmos layer, we can move the text farther out
        # to avoid clashes with text from levels below
        if self._is_outmost(path):
            if 0 <= angle < 90:
                va = "bottom"
                ha = "left"
            elif 90 <= angle <= 180:
                va = "bottom"
                ha = "right"
            elif 180 <= angle <= 270:
                va = "top"
                ha = "right"
            elif 270 <= angle <= 360:
                va = "top"
                ha = "left"
            else:
                raise ValueError
        else:
            ha = "center"
            va = "center"

        bbox_props = dict(boxstyle="round,pad=0.3", fc=(1,1,1,0.8),ec=(0.25,0.25,0.25,0.8), lw=0.5)

        text = "{} {}".format(self.path_text(path), self.format_value(self._completed_pv[path]))
        self.axes.text(mid_x, mid_y, text, ha=ha, va=va,
                       rotation=rotation, bbox=bbox_props)

    def _tangential_text(self, path):
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        level = len(path)
        radius = self._wedge_mid_radius(level)
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

        bbox_props = dict(boxstyle="round,pad=0.3", fc=(1,1,1,0.8),ec=(0.25,0.25,0.25,0.8), lw=0.5)

        text = "{}\n{}".format(self.path_text(path), self.format_value(self._completed_pv[path]))
        self.axes.text(mid_x, mid_y, text, ha="center",
                       va="center", rotation=rotation, bbox=bbox_props)

    def plot(self):
        if not self.wedges:
            # we didn't prepare the data yet
            self.prepare_data()
        for w in self.wedges:
            self.axes.add_patch(w)
        for path in self._paths:
            if len(path)*(self._angles[path].theta2 -
                          self._angles[path].theta1) > 90:
                # todo: random criteria!
                self._tangential_text(path)
            else:
                self._radial_text(path)

    def wedge(self, path):
        level = len(path)
        return Wedge((self.origin[0], self.origin[1]),
                     self._wedge_outer_radius(level),
                     self._angles[path].theta1,
                     self._angles[path].theta2,
                     width=self.wedge_width(level),
                     label=self.path_text(path),
                     facecolor=self.face_color(path),
                     edgecolor=self.edge_color(path),
                     fill=True)  # todo: supply rest of the arguments
