#!/usr/bin/env python3

from typing import List

STRING_DELIM = "/"


class Path(tuple):
    def __new__(cls, iterable):
        for t in iterable:
            assert isinstance(t, str)
            # this is e.g. important for paths2dot:
            assert STRING_DELIM not in t
        return super().__new__(cls, iterable)

    def __str__(self):
        # requires all entries of the underlying tuple to be strings!
        return STRING_DELIM.join(self)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        # return elements of type Path, not tuple!
        # (also affects slicing etc.)
        result = tuple.__getitem__(self, item)
        return Path(result)

    def startswith(self, tag):
        if not isinstance(tag, Path):
            raise ValueError("Must be Path instance!")
        if len(tag) > len(self):
            return False
        return tuple(tag) == tuple(self[:len(tag)])

    def parent(self):
        return self[:len(self) - 1]


def paths2dot(paths: List[Path], filename):
    with open(filename, "w") as out:
        # strict: don't draw multiple edges
        out.write("strict digraph G {")
        for path in paths:
            # Note: We have to make sure that a path like "1/1" is
            # interpreted as 1->"1/1"-and not as a loop, so we designate the
            #  vertices of the tree by the string representations of their
            # paths.
            path_steps = (path[:level + 1] for level in range(len(path)))
            vertex_names =  ('"{}"'.format(STRING_DELIM.join(step)) for step in
                             path_steps)
            out.write("\t{};\n".format('->'.join(vertex_names)))
        out.write("}")
