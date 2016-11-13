#!/usr/bin/env python3

import collections
from typing import Dict, List
from itertools import groupby
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from .path import Path


# future: sorting & unsorting

# fixme: problems with the total sum/value at the root
# (not the same, as value at root can be more than the total of the next level)
# solution: do not allow empty roots to be given by the user
# thus the real (empy) root always carries the total sum of the entries
# and gets set by complete
# to plot the innerst circle, bring back the draw_center_circle option

def complete(pathvalues: Dict[Path, float]) -> Dict[Path, float]:
    """ Consider a pathvalue dictionary of the form Dict[Path, float] e.g.
    {1.1.1: 12.0} (here: only one entry). This function will disect each path
    and assign its value to the truncated path: e.g. here 1, 1.1 and 1.1.1.
    Thus we get {1: 12.0, 1.1: 12.0, 1.1.1: 12.0}. For more items the values
    will be summed accordingly.
    Furthermore the total sum of the items of
    the topmost level will be assigned to the empty path. For this to make
    sense we require that no empy path is in the pathvalues beforehand""
    :param pathvalues: {path: value} dictionary :return: {path: value}
    dictionary
    """
    if Path(()) in pathvalues:
        raise ValueError("This function does not allow the empty path as item"
                         "in the pathvalues list.")
    completed = collections.defaultdict(float)
    for path, value in pathvalues.items():
        # len(path) +1 ensures that also the whole tag is considered
        # starting point 0: also add to empty path.
        for level in range(0, len(path) + 1):
            completed[path[:level]] += value
    return completed


def structurize(paths: List[Path]) -> List[List[List[Path]]]:
    """ Takes a list of paths and groups the paths first by length (empty
    path length 0) and then by the parent (path[:len(path) - 1]).
    Example:
    [
        [ ["" ]],                    # the root
        [ [1, 2, 3] ],               # level 1: only one group, because all
                                     #   elements share the same parent
        [ [1.1, 1.2], [3.1, 3.2] ],  # grouped by parents
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

    # sort by level
    paths.sort(key=level)
    paths_by_level = (list(group) for _, group in groupby(paths, key=level))

    # sort by parent
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
                 pathvalues: Dict[Path, float],
                 axes,
                 origin=(0, 0),
                 cmap=plt.get_cmap('autumn'),
                 default_ring_width=0.4,
                 default_edge_color=(0, 0, 0, 1),
                 default_line_width=1,
                 plot_center=False,
                 plot_minimal_angle=0,
                 label_minimal_angle=0):
        """

        :param pathvalues: Dict[Path, float]
        :param axes:
        :param origin: Coordinates of the center of the pie chart.
        :param cmap: Colormap: Controls the coloring based on the angle.
        :param default_ring_width: Default width of each ring/wedge.
        :param default_edge_color: Default edge color of the wedges.
        :param default_line_width: Default line width of the wedges.
        :param plot_center: Plot a circle in the middle corresponding to the
                            total of all paths.
        :param plot_minimal_angle: Plot only wedges with an angle bigger
                                   than plot_minimal_angle
        :param label_minimal_angle: Only label wedges with an angle bigger than
                                    plot_minimal_angle
        """

        # *** Input & Config *** (emph)
        self.input_pv = pathvalues
        self.axes = axes
        self.cmap = cmap
        self.origin = origin
        self.default_ring_width = default_ring_width
        self.default_edge_color = default_edge_color
        self.default_line_width = default_line_width
        self.plot_center = plot_center
        self.plot_minimal_angle = plot_minimal_angle
        self.label_minimal_angle = label_minimal_angle

        # *** Variables used for computation *** (emph)
        self._completed_pv = None        # type: Dict[Path, float]
        self._paths = None               # type: List[Path]
        self._max_level = None           # type: int
        self._structured_paths = None    # type: List[List[List[Path]]]
        self._angles = None              # type: Dict[Path, Angles]

        # *** "Output" *** (emph)
        self.wedges = {}                 # type: Dict[Path, Wedge]

    def prepare_data(self):
        """ Sets up auxiliary variables.
        """
        self._completed_pv = complete(self.input_pv)
        self._paths = list(self._completed_pv.keys())
        self._max_level = max((len(path) for path in self._paths))
        self._structured_paths = structurize(self._paths)
        self._angles = calculate_angles(self._structured_paths,
                                        self._completed_pv)

        for path in self._paths:
            if self.plot_center or len(path) >= 1:
                angle = self._angles[path].theta2 - self._angles[path].theta1
                if len(path) == 0 or angle > self.plot_minimal_angle:
                    self.wedges[path] = self.wedge(path)

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

    # noinspection PyUnusedLocal
    def wedge_width(self, path: Path):
        """
        The width to a ring/wedge.
        :param path:
        :return:
        """
        return self.default_ring_width

    # noinspection PyUnusedLocal
    def wedge_gap(self, path: Path):
        return 0, 0

    def _wedge_outer_radius(self, path: Path):
        """ The outer radius of the wedge corresponding to a path.
        This method takes path as an argument (and not len(path)) to allow
        to explode slices.
        :param path
        :return
        """
        return self._wedge_inner_radius(path) + self.wedge_width(path)

    def _wedge_inner_radius(self, path: Path):
        """ The inner radius of the wedge corresponding to a path.
        This method takes path as an argument (and not len(path)) to allow
        to explode slices.
        :param path
        :return
        """
        start = 0 if self.plot_center else 1
        ancestors = [path[:i] for i in range(start, len(path))]
        return sum(self.wedge_width(ancestor) + sum(self.wedge_gap(ancestor))
                   for ancestor in ancestors) + self.wedge_gap(path)[0]

    def _wedge_mid_radius(self, path: Path):
        """ The radius of the middle of the wedge corresponding to a path.
        This method takes path as an argument (and not len(path)) to allow
        to explode slices.
        :param path
        :return
        """
        return (self._wedge_outer_radius(path) +
                self._wedge_inner_radius(path)) / 2

    # noinspection PyUnusedLocal
    def edge_color(self, path):
        return self.default_edge_color

    # noinspection PyUnusedLocal
    def line_width(self, path):
        return self.default_line_width

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

    # noinspection PyMethodMayBeStatic
    def format_path_text(self, path):
        return path[-1] if path else ""

    # noinspection PyMethodMayBeStatic
    def format_value_text(self, value):
        return "{0:.2f}".format(value)
        # todo:
        # hours = int(value/60)
        # minutes = int(value - hours * 60)
        # if hours:
        #     return "({}h{})".format(hours, minutes)
        # else:
        #     return "({})".format(minutes)

    def text(self, path, value):
        path_text = self.format_path_text(path)
        value_text = self.format_value_text(value)
        if path_text and value_text:
            return "{} ({})".format(path_text, value_text)
        return path_text

    def _radial_text(self, path):
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self._wedge_mid_radius(path)
        if self._is_outmost(path):
            radius = self._wedge_inner_radius(path)

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

        # todo: allow customization
        bbox_props = dict(boxstyle="round,pad=0.3", fc=(1, 1, 1, 0.8),
                          ec=(0.25, 0.25, 0.25, 0.8), lw=0.5)

        text = self.text(path, self._completed_pv[path])
        self.axes.text(mid_x, mid_y, text, ha=ha, va=va,
                       rotation=rotation, bbox=bbox_props)

    def _tangential_text(self, path):
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self._wedge_mid_radius(path)
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

        # todo: allow customization
        bbox_props = dict(boxstyle="round,pad=0.3", fc=(1, 1, 1, 0.8),
                          ec=(0.25, 0.25, 0.25, 0.8), lw=0.5)

        text = self.text(path, self._completed_pv[path])
        self.axes.text(mid_x, mid_y, text, ha="center",
                       va="center", rotation=rotation, bbox=bbox_props)

    def plot(self, setup_axes=False):
        if not self.wedges:
            # we didn't prepare the data yet
            self.prepare_data()
        for path, wedge in self.wedges.items():
            self.axes.add_patch(wedge)
            angle = self._angles[path].theta2 - self._angles[path].theta1

            if not angle > self.label_minimal_angle:
                # no text
                continue

            if len(path)*angle > 90:
                # fixme: replace with less random criteria!
                self._tangential_text(path)
            else:
                self._radial_text(path)

        if setup_axes:
            self.axes.autoscale()
            self.axes.set_aspect("equal")
            self.axes.autoscale_view(True, True, True)
            self.axes.get_xaxis().set_visible(False)
            self.axes.get_yaxis().set_visible(False)
            self.axes.margins(x=0.1, y=0.1)

    def wedge(self, path):
        level = len(path)
        return Wedge((self.origin[0], self.origin[1]),
                     self._wedge_outer_radius(path),
                     self._angles[path].theta1,
                     self._angles[path].theta2,
                     width=self.wedge_width(path),
                     label=self.text(path, self._completed_pv[path]),
                     facecolor=self.face_color(path),
                     edgecolor=self.edge_color(path),
                     linewidth=self.line_width(path),
                     fill=True)  # todo: supply rest of the arguments
