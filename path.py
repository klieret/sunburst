#!/usr/bin/env python3


class Path(tuple):
    def __new__(cls, iterable):
        for t in iterable:
            assert isinstance(t, str)
        return super().__new__(cls, iterable)

    def __str__(self):
        # requires all entries of the underlying tuple to be strings
        return ":".join(self)

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


