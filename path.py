#!/usr/bin/env python3

from typing import List

STRING_DELIM = "/"


class Path(tuple):
    def __new__(cls, iterable):
        for t in iterable:
            assert isinstance(t, str)
        return super().__new__(cls, iterable)

    def __str__(self):
        # requires all entries of the underlying tuple to be strings!
        # __str__() should be readable, __repr__() should be unique
        return STRING_DELIM.join(self)

    def __repr__(self):
        # __str__() should be readable, __repr__() should be unique
        # ==> use quotation marks. Since the string itself can also contain
        # various kinds of quote constructions, just use the __repr__ method
        # of the str class.
        return STRING_DELIM.join((string.__repr__() for string in self))

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


def paths2dot(paths: List[Path], full_labels=True) -> str:
    """ Converts a list of paths to their correspondent graph described in the
    DOT language (see http://www.graphviz.org/doc/info/lang.html). Not using
    the python graphviz package to reduce dependencies.
    :param paths: List of paths.
    :param full_labels: If true, the vertices of the graph are labeled with the
                        full path, else only the name of the endpoint
                        (path[:-1]) is printed.
    :return: graph described in DOT language as string.
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

        vertices = [path[:level + 1] for level in range(len(path))]
        vertex_ids = (vid(vertex) for vertex in vertices)
        dot += "\t{};\n".format('->'.join(vertex_ids))
        # since __repr__ has a lot of quotation marks mixed in the
        # representation, we adapt the labeling with the ouput of __str__
        # we have to manually escape double quotation marks)
        for vertex in vertices:
            if full_labels:
                label = str(vertex).replace('"', '\\"')
            else:
                label = str(vertex[-1]).replace('"', '\\"')
            dot += '\t{} [label="{}"];\n'.format(vid(vertex), label)
    dot += "}"
    return dot
