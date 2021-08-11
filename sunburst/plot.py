#!/usr/bin/env python3

from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from sunburst.calc import (
    complete_pv,
    complete_paths,
    structure_paths,
    calculate_angles,
    Angles,
)
from sunburst.path import Path


class SunburstPlot(object):
    """The central class of the suburst package.

    Usage:
        - Initialize SunburstPlot object
        - Redefine attributes or methods
        - Run SunburstPlot.plot()

    All of the following attributes can be set
        - as keyword argument during initialisation
        - after initialization, but before calling :py:meth:`.prepare_data`
          or :py:meth:`.plot`.

    Arguments starting with the prefix `base` can also be defined
    dynamically (usually depending on the path to which a wedge correspond)
    by redefining the method with the same name without the prefix `base`.

    E.g. the attribute :py:attr:`.self.base_wedge_width` corresponds to the
    initialization keyword argument `base_wedge_width` and to the method
    :py:meth:`.wedge_width`: ::

        def wedge_width(self, path: Path) -> float:
            return self.base_ring_width

    Almost all of the methods can (or are meant to) be redefined.
    Those which should be handled more carefully are designated by a leading
    underscore.

    Attributes:
        pathvalues: pathvalues of type
            MutuableMapping[Path, float]
        axes:
        origin: Coordinates of the center of the pie chart as tuple
        cmap: Colormap: Controls the coloring based on the angle.
        base_ring_width: Default width of each ring/wedge.
        base_edge_color: Default edge color of the wedges.
        base_line_width: Default line width of the wedges.
        plot_center: Plot a circle in the middle corresponding to the
            total of all paths.
        plot_minimal_angle: Plot only wedges with an angle bigger
            than plot_minimal_angle
        label_minimal_angle: Only label wedges with an angle bigger than
            this value
        order: string with syntax keep|value|key [reverse], e.g.
           "key reverse" (default) or "value" or "reverse"
           controlling in which order the wedges will be created

           - keep: Keep the order of the supplied pathvalues
             dictionary (for this to work, use a dictionary
             subclass that supports ordering, i.e.
             collections.OrderedDict). This is the default, but
             explicitly stating it, will warn you if you supply a
             normal dict for pathvalues.
           - value: Sort values from small to big
           - key: Sort paths alphabetically
           - reversed: take the order specified by one of the above
             options (or none) and reverse it.
        base_textbox_props: Properties of the textbox (bbox) that annotating
            the wedge corresponding to `path`. See
            http://matplotlib.org/users/annotations_guide.html
    """

    def __init__(
        self,
        input_pv: Dict[Path, float],
        axes,  # todo: make optional argument?
        origin=(0.0, 0.0),
        cmap=plt.get_cmap("autumn"),
        base_ring_width=0.4,
        base_edge_color=(0, 0, 0, 1),
        base_line_width=0.75,
        plot_center=False,
        plot_minimal_angle=0,
        label_minimal_angle=0,
        order="value reverse",
        base_textbox_props=None,
    ):

        # *** Input & Config ***                                        (emph)
        self.input_pv = input_pv
        self.axes = axes
        self.cmap = cmap
        self.origin = origin
        self.base_wedge_width = base_ring_width
        self.base_edge_color = base_edge_color
        self.base_line_width = base_line_width
        self.plot_center = plot_center
        self.plot_minimal_angle = plot_minimal_angle
        self.label_minimal_angle = label_minimal_angle
        self.order = order
        self.base_textbox_props = base_textbox_props
        if not base_textbox_props:
            self.base_textbox_props = dict(
                boxstyle="round, pad=0.2",
                fc=(1, 1, 1, 0.8),
                ec=(0.4, 0.4, 0.4, 1),
                lw=0.0,
            )

        # *** Variables used for computation ***                        (emph)
        self._completed_pv = {}  # type: Dict[Path, float]
        self._completed_paths = []  # type: List[Path]
        self._max_level = 0  # type: int
        self._structured_paths = []  # type: List[List[List[Path]]]
        self._angles = {}  # type: Dict[Path, Angles]

        # *** "Output" *** (emph)
        self.wedges = {}  # type: Dict[Path, Wedge]

    def prepare_data(self) -> None:
        """Sets up auxiliary variables.

        Most of the actual computations are defined as functions for better
        testing (in file :file:`calc.py`).
        """

        # todo: maybe join together with self.plot?
        # todo maybe split up more....
        # even if self.input_pv is of type OrderedDict,
        # self._completed_pv will be a normal (unsorted) dictionary
        self._completed_pv = complete_pv(self.input_pv)

        # Complete the list of paths with possible missing ancestors:
        # Do not take the keys of self._completed_pv, because they will
        # not be sorted anymore. The sorting of self._completed_paths
        # induces the sorting of self._structured_paths which is
        # responsible for the order of the wedges.
        ordered_paths: List[Path] = []

        if self.order:
            order_options = set(self.order.split(" "))
        else:
            order_options = set()

        # check supplied order options:                                 (emph)
        lonely_order_options = {"value", "key", "keep"}
        allowed_order_options = lonely_order_options | {"reverse"}
        if not order_options <= allowed_order_options:
            raise ValueError(
                "'order' option must consist of a subset of "
                "strings from {}, joined by "
                "spaces.".format(allowed_order_options)
            )
        if not len(order_options & lonely_order_options) <= 1:
            raise ValueError(
                "Only one of the options {} "
                "allowed.".format(lonely_order_options)
            )

        if not order_options:
            ordered_paths = list(self.input_pv.keys())
        elif "keep" in self.order:
            ordered_paths = list(self.input_pv.keys())
            if type(self.input_pv) is dict:
                # do not use isinstance (because this would yield true for
                # a OrderedDict or any other (possibly ordered subclass of dict
                # as well)
                print(
                    "Warning: Looks like you want to keep the order of your"
                    "input pathvalues, but pathvalues are of type dict "
                    "which does keep record of the order of its items."
                )
        elif "value" in self.order:
            ordered_paths = sorted(
                self._completed_pv.keys(),
                key=lambda key: self._completed_pv[key],
            )
        elif "key" in self.order:
            ordered_paths = sorted(self._completed_pv.keys())
        if "reverse" in self.order:
            ordered_paths = list(reversed(ordered_paths))

        self._completed_paths = complete_paths(ordered_paths)

        self._max_level = max((len(path) for path in self._completed_paths))

        # the order of self._structured paths determines the
        # arrangement of the wedges afterwards.
        self._structured_paths = structure_paths(self._completed_paths)

        self._angles = calculate_angles(
            self._structured_paths, self._completed_pv
        )

        for path in self._completed_paths:
            if self.plot_center or len(path) >= 1:
                angle = self._angles[path].theta2 - self._angles[path].theta1
                if len(path) == 0 or angle > self.plot_minimal_angle:
                    self.wedges[path] = self.wedge(path)

    def _is_outmost(self, path: Path) -> bool:
        """Returns True if the wedge corresponding to `path` is the
        "outmost" wedge, i.e. there is no descendant of `path`.
        """
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
    def wedge_width(self, path: Path) -> float:
        """The width of the wedge corresponding to `path`.

        This method is meant to be redefined. Per default it only returns
        :py:attr:`base_wedge_width`.
        """
        return self.base_wedge_width

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def wedge_spacing(self, path: Path) -> Tuple[float, float]:
        """The radial space before the wedge corresponding to `path` and
        after.

        E.g. if `wedge_space(some/path) = 0.1, 0.2`, then this shifts the wedge
        corresponding to some/path by 0.1 radially away from the center and all
        wedges corresponding to ancestors of some/path (e.g. some/path/child,
        some/path/child/grandchild) by 0.2 radially away from the center.
        """
        return 0, 0

    def _wedge_outer_radius(self, path: Path) -> float:
        """The outer radius of the wedge corresponding to a path.

        Instead of redefining this method, adapt :py:meth:`.wedge_width` resp.
        :py:meth:`.wedge_width`.
        """
        return self._wedge_inner_radius(path) + self.wedge_width(path)

    def _wedge_inner_radius(self, path: Path) -> float:
        """The inner radius of the wedge corresponding to a path.

        Instead of redefining this method, adapt :py:meth:`.wedge_width` resp.
        :py:meth:`.wedge_width`.
        """
        start = 0 if self.plot_center else 1
        ancestors = [path[:i] for i in range(start, len(path))]
        return (
            sum(
                self.wedge_width(ancestor) + sum(self.wedge_spacing(ancestor))
                for ancestor in ancestors
            )
            + self.wedge_spacing(path)[0]
        )

    def _wedge_mid_radius(self, path: Path) -> float:
        """The radius of the middle of the wedge corresponding to a path.

        Instead of redefining this method, adapt :py:meth:`.wedge_width` resp.
        :py:meth:`.wedge_width`.
        """
        return (
            self._wedge_outer_radius(path) + self._wedge_inner_radius(path)
        ) / 2

    # noinspection PyUnusedLocal
    def edge_color(self, path: Path) -> Tuple[float, float, float, float]:
        """The line color of the wedge corresponding to `path`.

        This method is meant to be redefined. Per default it only returns
        :py:attr:`base_edge_color`."""
        return self.base_edge_color

    # noinspection PyUnusedLocal
    def line_width(self, path: Path) -> float:
        """The line width of the wedge corresponding to `path`.

        This method is meant to be redefined. Per default it only returns
        :py:attr:`base_line_width`."""
        return self.base_line_width

    def face_color(self, path: Path) -> Tuple[float, float, float, float]:
        """The color of the wedge corresponding to `path`.

        Per default, the color is calculated by the value of
        :py:attr:`.cmap` at the mid-angle of the wedge. The color of an
        inner circle (corresponding to an empty `path`) is always set to be
        white. Colors a slightly brightened with increasing level.
        """
        # take the middle angle, else the first wedge will have the same color
        # as its parent or at least make sure, that we don't get the value 0
        # (white or black in a lot of color maps)
        if len(path) == 0:
            color: List[float] = [1, 1, 1, 1]
        else:
            angle = (self._angles[path].theta1 + self._angles[path].theta2) / 2
            color = list(self.cmap(angle / 360))  # type: ignore
            # make the color get lighter with increasing level
            for i in range(3):
                color[i] += (
                    (1 - color[i]) * 0.7 * (len(path) / (self._max_level + 1))
                )
            # somehow the following seems to be ignored yet
            # color[3] = 1 - (len(path) - 1)**3 / (self._max_level**3 )
            # print(color[3])
        return tuple(color)  # type: ignore

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def alpha(self, path: Path) -> float:
        """The alpha value of the wedge corresponding to `path`.

        This method is meant to be redefined. Per default it only returns 1.
        """
        return 1

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def textbox_props(self, path: Path, text_type: str) -> Dict:
        """Properties of the textbox (bbox) that annotating the wedge
        corresponding to `path`.

        This method is meant to be redefined. Per default it is independent
        of the arguments.

        Args:
            path (Path): path
            text_type (str): Position type of the text box:
                "tangential", "radial", etc.

        Returns:
            Dictionary of keyword properties for the bbox option of the
            :py:meth:`matplotlib.pyplot.text` function.
            See http://matplotlib.org/users/annotations_guide.html
        """
        return self.base_textbox_props

    # noinspection PyMethodMayBeStatic
    def format_path_text(self, path) -> str:
        """Returns a string representation for `path` which is used to
        annotate the corresponding wedge.
        """
        return path[-1] if path else ""

    # noinspection PyMethodMayBeStatic
    def format_value_text(self, value: float) -> str:
        """Returns a string representation of the value corresponding to
        `path` which is used to annotate the wedge corresponding to
        `path`.
        """
        return "{0:.2f}".format(value)
        # todo:
        # hours = int(value/60)
        # minutes = int(value - hours * 60)
        # if hours:
        #     return "({}h{})".format(hours, minutes)
        # else:
        #     return "({})".format(minutes)

    def format_text(self, path: Path) -> str:
        """Returns a string used annotate the wedge corresponding to `path`.

        Most modifications of the annotations can be made by redefining
        :py:meth:`.format_path_text` or :py:meth:`.format_value_text`, this
        method combines both of those methods.
        """
        path_text = self.format_path_text(path)
        value_text = self.format_value_text(self._completed_pv[path])
        if path_text and value_text:
            return "{} ({})".format(path_text, value_text)
        return path_text

    def _radial_text(self, path: Path) -> None:
        """Adds a radially rotated annotation for the wedge corresponding to
        `path` to the axes.
        """
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
            # note that a rotation around 360 flips the text, so
            # the -360 does matter.
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

        text = self.format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha=ha,
            va=va,
            rotation=rotation,
            bbox=self.textbox_props(path, "radial"),
        )

    def _tangential_text(self, path: Path) -> None:
        """Adds a tangentially rotated annotation for the wedge corresponding to
        `path` to the axes.
        """
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

        text = self.format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha="center",
            va="center",
            rotation=rotation,
            bbox=self.textbox_props(path, "tangential"),
        )

    def _add_annotation(self, path):
        """Adds annotation to the wedge corresponding to `path`."""
        angle = self._angles[path].theta2 - self._angles[path].theta1

        if not angle > self.label_minimal_angle:
            # no text
            return

        # fixme: replace with less random criteria!
        if len(path) * angle > 90:
            self._tangential_text(path)
        else:
            self._radial_text(path)

    def plot(self, setup_axes=False, interactive=False) -> None:
        """Method that combines several others, to do all necessary
        preparations and add the plot to the axes :py:attr:`self.axes`.

        Args:
            setup_axes (bool): Does some basic setup for the axes
               (autoscale, margins, etc.). It won't always be the perfect setup
               but it saves writing a few lines.
            interactive (bool): Display label for the wedge under the cursor
                only.
        """
        if not self.wedges:
            # we didn't prepare the data yet
            self.prepare_data()
        for path, wedge in self.wedges.items():
            self.axes.add_patch(wedge)
            if not interactive:
                self._add_annotation(path)

        if setup_axes:
            self.axes.autoscale()
            self.axes.set_aspect("equal")
            self.axes.autoscale_view(True, True, True)
            self.axes.axis("off")
            self.axes.margins(x=0.1, y=0.1)

        if interactive:

            def hover(event):
                if event.inaxes == self.axes:
                    found = False
                    for path in self.wedges:
                        if not found:
                            cont, ind = self.wedges[path].contains(event)
                        else:
                            cont = False
                        if cont:
                            self.wedges[path].set_alpha(0.5)
                            self.axes.set_title(self.format_text(path))
                        else:
                            self.wedges[path].set_alpha(1.0)
                    self.axes.figure.canvas.draw_idle()

            self.axes.figure.canvas.mpl_connect("motion_notify_event", hover)

    def wedge(self, path: Path) -> Wedge:
        """Generates the patches wedge object corresponding to `path`."""
        return Wedge(
            (self.origin[0], self.origin[1]),
            self._wedge_outer_radius(path),
            self._angles[path].theta1,
            self._angles[path].theta2,
            width=self.wedge_width(path),
            label=self.format_text(path),
            facecolor=self.face_color(path),
            edgecolor=self.edge_color(path),
            linewidth=self.line_width(path),
            fill=True,
            alpha=self.alpha(path),
        )
        # todo: supply rest of the arguments
