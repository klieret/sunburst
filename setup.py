#!/usr/bin/env python3

""" To install this package, change to the directory of this file and run

    pip3 install --user .

(the ``--user`` flag installs the package for your user account only, otherwise
you will need administrator rights).
"""

# std
import site
import sys
import setuptools

# Sometimes editable install fails with an error message about user site
# being not writeable. The following line can fix that, see
# https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]


if __name__ == "__main__":
    setuptools.setup()
