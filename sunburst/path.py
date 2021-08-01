#!/usr/bin/env python3

from typing import List, Iterable, Dict, Any
from collections import OrderedDict

STRING_DELIM = "/"


class Path(tuple):
    def __new__(cls, iter_: Iterable[str]):
        for item in iter_:
            assert isinstance(item, str)
        return super().__new__(cls, iter_)  # type: ignore

    def __str__(self) -> str:
        # requires all entries of the underlying tuple to be strings!
        # __str__() should be readable, __repr__() should be unique
        return STRING_DELIM.join(self)

    def __repr__(self) -> str:
        # __str__() should be readable, __repr__() should be unique
        # ==> use quotation marks. Since the string itself can also contain
        # various kinds of quote constructions, just use the __repr__ method
        # of the str class.
        # This should normally return code that can directly interpreted
        # by python to give the same Path element than the string
        # represents
        return "Path(({}, ))".format(
            ", ".join((string.__repr__() for string in self))
        )

    def __getitem__(self, key):
        result = tuple.__getitem__(tuple(self), key)
        # todo: is this good style? Stands in contrast to the behaviour of other
        #  iterators...
        # Depending on whether key was a single int or a slice object ,
        # tuple.__getitem__ will return a tuple or a string. However,
        # we want our __getitem__ method to return a Path instance in either
        # way!
        if isinstance(result, tuple):
            return Path(result)
        elif isinstance(result, str):
            return Path((result,))  # do not remove ',' or it's gonna be a str

    def startswith(self, tag):
        if not isinstance(tag, Path):
            raise ValueError(
                "Expecting instance of Path " "but got {}!".format(type(tag))
            )
        if len(tag) > len(self):
            return False
        return self[: len(tag)] == tag

    def parent(self):
        return self[: len(self) - 1]

    def ancestors(self):
        return [self[:i] for i in range(len(self) + 1)]


def paths2dot(paths: List[Path], full_labels=True) -> str:
    """Converts a list of numbering to their correspondent graph described in
    the     DOT language (see http://www.graphviz.org/doc/info/lang.html).
    Not using the python graphviz package to reduce dependencies.

    Args:
        paths: List of numbering.
        full_labels: If true, the vertices of the graph are labeled with the
            full path, else only the name of the endpoint (path[:-1]) is
            printed.

    Returns:
        graph described in DOT language as string.
    """
    dot = ""  # return value
    # strict: don't draw multiple edges
    dot += "strict digraph G {"
    for path in paths:
        # Note: We have to make sure that a path like "1/1" is interpreted
        # as 1->"1/1"-and not as a loop of the vertex "1", so we designate
        # the vertices of the tree by the positive hashes of the path object
        def vid(vert):
            return str(abs(hash(vert)))

        vertices = [path[: level + 1] for level in range(len(path))]
        vertex_ids = (vid(vertex) for vertex in vertices)
        dot += "\t{} [dir=none];\n".format("->".join(vertex_ids))
        # since __repr__ has a lot of quotation marks mixed in the
        # representation, we adapt the labeling with the output of __str__
        # we have to manually escape double quotation marks)
        for vertex in vertices:
            if full_labels:
                label = str(vertex).replace('"', '\\"')
            else:
                label = str(vertex[-1]).replace('"', '\\"')
            dot += '\t{} [label="{}"];\n'.format(vid(vertex), label)
    dot += "}"
    return dot


def stringvalues_to_pv(
    stringvalues: Dict[str, float], delim=STRING_DELIM
) -> Dict[Path, float]:
    assert all(isinstance(item, str) for item in stringvalues.keys())
    return {
        Path(item.split(delim)): value for item, value in stringvalues.items()
    }


def stringlist_to_ordered_pv(
    stringpairs: List[Any], delim=STRING_DELIM
) -> Dict[Path, float]:
    keys = stringpairs[::2]
    values = stringpairs[1::2]
    assert all(isinstance(item, str) for item in keys)
    assert all(isinstance(item, float) for item in values)
    paths = [Path(item.split(delim)) for item in keys]
    return OrderedDict(zip(paths, values))


def charvalues_to_pv(charvalues: Dict[str, float]) -> Dict[Path, float]:
    assert all(isinstance(item, str) for item in charvalues.keys())
    return {Path(tuple(item)): value for item, value in charvalues.items()}


def charlist_to_ordered_pv(
    stringpairs: List[Any],
) -> Dict[Path, float]:
    keys = stringpairs[::2]
    values = stringpairs[1::2]
    assert all(isinstance(item, str) for item in keys)
    assert all(isinstance(item, float) for item in values)
    paths = [Path(tuple(item)) for item in keys]
    return OrderedDict(zip(paths, values))
