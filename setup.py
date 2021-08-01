#!/usr/bin/env python3

# std
from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools  # see below (1)

# (1) see https://stackoverflow.com/questions/8295644/
# Without this import, install_requires won't work.

import site
import sys

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

packages = setuptools.find_packages()


setup(
    name="sunburst",
    description="Hierarchical Pie charts for pyplot",
    author="klieret",
    author_email="kilian.lieret@posteo.de",
    url="https://github.com/klieret/pyplot-hierarchical-pie",
    packages=packages,
    install_requires=["matplotlib"],
    license="BSD",
)
