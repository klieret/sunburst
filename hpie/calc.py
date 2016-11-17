#!/usr/bin/env python3

import collections
from itertools import groupby
from typing import Dict, List
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
    sense we require that no empy path is in the data beforehand""
    :param pathvalues: {path: value} dictionary :return: {path: value}
    dictionary
    """
    if Path(()) in pathvalues:
        raise ValueError("This function does not allow the empty path as item"
                         "in the data list.")
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


# todo: docstring . path values must be complete!
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
